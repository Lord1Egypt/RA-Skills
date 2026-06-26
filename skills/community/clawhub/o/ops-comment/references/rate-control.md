# 速率控制 v2.0 — 基于规则的执行指南

## 一、总体架构

速率控制由以下规则组成，按优先级执行：

```
1. 每日硬限额 → 到达即停，不可突破
2. 会话时长限制 → 到时即停
3. 动作间隔 → 每两个动作间的最小等待
4. 随机抖动 → 叠加在基准间隔上的随机偏移
5. 连续动作检测 → 防止同类动作连发
6. 定期休息 → 每 N 次动作后强制暂停
7. 会话节奏 → 开头慢→中间正常→结尾慢
```

---

## 二、每日硬限额

### 2.1 限额值

| 动作 | 默认限额 | 养号期 | 增长期 | 绝对上限 |
|------|---------|-------|-------|---------|
| 点赞 | 120 | 60 | 120 | 200 |
| 收藏 | 30 | 15 | 30 | 50 |
| 关注 | 25 | 10 | 25 | 30 |
| 评论 | 15 | 5 | 15 | 20 |
| 总计 | 150 | 70 | 150 | 250 |

### 2.2 限额检查方式

每次执行动作前，从日志文件读取今日计数：
```
Bash: grep -c '"action":"like","success":true' data/nurture-log/YYYY-MM-DD.jsonl 2>/dev/null || echo 0
```

如果 count >= limit → 跳过该类动作。
如果 total >= total_limit → 结束会话。

### 2.3 绝对上限

即使用户修改配置，也**不可**超过 `safety_max` 中定义的绝对上限。
在读取配置后立即校验：`actual_limit = min(user_config, absolute_max)`

---

## 三、动作间隔

### 3.1 基准间隔表

| 动作转换 | 最小间隔(秒) | 最大间隔(秒) |
|---------|------------|------------|
| 点赞 → 点赞 | 8 | 30 |
| 点赞 → 收藏（同一笔记） | 5 | 20 |
| 点赞 → 关注 | 30 | 120 |
| 收藏 → 任何 | 10 | 40 |
| 关注 → 任何 | 60 | 180 |
| 评论 → 任何 | 90 | 300 |
| 任何 → 评论 | 60 | 180 |

### 3.2 计算实际间隔

```
1. 查表获取 [MIN, MAX] 范围
2. 生成随机间隔：
   javascript_tool("Math.floor(Math.random() * (MAX - MIN) + MIN)")
3. 叠加会话节奏倍数（见第六节）
4. 最终间隔 = random_interval × pace_multiplier
5. 执行：computer(action="wait", duration=最终间隔)
```

### 3.3 高斯模式（可选）

如果配置 `jitter.type == "gaussian"`，使用 Box-Muller 变换：
```
javascript_tool(`
  var base = (MIN + MAX) / 2;
  var std = base * 0.3;
  var u1 = Math.random(), u2 = Math.random();
  var z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  Math.max(Math.floor(base + z * std), MIN)
`)
```

高斯模式的好处：大多数间隔集中在中间值附近，偶尔出现较短或较长间隔，更接近真人行为模式。

---

## 四、连续动作限制

### 4.1 连续点赞限制

```
追踪连续点赞次数（在当前工作记忆中维护）

如果连续点赞达到 max_consecutive_likes (默认5)：
  → 必须插入一段纯浏览行为
  → 浏览时长：javascript_tool("Math.floor(Math.random() * 60 + 30)") 秒
  → 浏览内容：scroll 2-5 屏，可以打开 1 个笔记但不互动
  → 浏览完毕后重置连续计数

如果纯浏览的时长用 wait 实现，分多段执行（不要一次 wait 90秒）：
  wait 15-20秒 → scroll → wait 10-15秒 → scroll → wait 10-20秒
```

### 4.2 连续动作限制

```
连续互动动作（点赞/收藏/关注/评论，不含纯浏览）：
  max_consecutive_actions (默认8)

达到后：
  → 强制浏览休息 60-120 秒
  → 行为同上（滚动 + 看笔记 + 不互动）
```

---

## 五、定期休息

### 5.1 小休息（Cooldown）

```
每完成 cooldown_after_actions (默认20) 次互动动作：
  → 强制休息
  → 时长：javascript_tool("Math.floor(Math.random() * 180 + 120)") 秒（2-5分钟）
  → 休息期间：纯浏览行为
     - 回到首页浏览推荐流
     - 或者打开"通知"页面看看
     - 或者查看自己的主页
```

### 5.2 中场大休息

```
每 15-20 分钟（随机）：
  → 检查时间：javascript_tool("Date.now()") 与会话开始时间比较
  → 休息时长：javascript_tool("Math.floor(Math.random() * 300 + 180)") 秒（3-8分钟）
  → 休息行为：
     - 可以去看看与主题无关的内容（首页推荐）
     - 可以不操作（模拟用户去喝水/上厕所）
     - 可以点开个人主页看看自己的数据
```

---

## 六、会话节奏曲线

### 6.1 节奏倍数

根据会话已进行的时间比例，调整间隔倍数：

```
elapsed_ratio = (当前时间 - 开始时间) / 计划总时长

间隔倍数：
  ratio < 0.10  → ×2.0  (预热期，纯浏览，不互动)
  ratio < 0.25  → ×1.5  (渐入状态)
  ratio < 0.75  → ×1.0  (活跃期)
  ratio < 0.90  → ×1.3  (开始疲劳)
  ratio >= 0.90 → ×2.5  (收尾期)
```

### 6.2 收尾处理

```
当 elapsed_ratio >= 0.90：
  - 最后 3-5 个动作，间隔翻倍
  - 更多浏览，更少互动
  - 最后一个动作完成后：
    → 纯浏览 1-3 分钟
    → 可以去首页随便看看
    → 然后结束会话
```

---

## 七、会话时长

### 7.1 时长计算

```
会话开始时记录时间：
  start_time = javascript_tool("Date.now()")

每次动作前检查是否超时：
  current_time = javascript_tool("Date.now()")
  elapsed_minutes = (current_time - start_time) / 60000
  
  如果 elapsed_minutes >= config.session.max_duration_minutes：
    → 进入收尾流程
  如果 elapsed_minutes >= config.safety_max.session_minutes：
    → 立即结束（绝对上限）
```

### 7.2 动态会话时长

不要每次都用同样的时长。会话开始时随机确定本次时长：
```
base = config.session.max_duration_minutes
actual = javascript_tool(`Math.floor(${base} * (0.7 + Math.random() * 0.3))`)
# 实际时长为配置值的 70%-100%
```

---

## 八、异常情况下的速率调整

### 8.1 出现 Medium 级风控信号

```
首次出现 → 所有间隔 ×2.0，持续到会话结束
再次出现 → 暂停 15 分钟
第三次 → 终止会话
```

### 8.2 连续失败

```
连续 3 个动作验证失败（按钮无响应/状态未变化）：
  → 暂停 2-3 分钟
  → 截图检查页面状态
  → 如果页面正常 → 继续（间隔 ×1.5）
  → 如果页面异常 → 终止会话
```

### 8.3 上下文压缩恢复

```
如果因上下文压缩丢失了计数器状态：
  → 从 JSONL 日志重新读取计数
  → 如果日志也不可用 → 保守估计，假设已执行50%配额
  → 继续执行时使用更保守的间隔（×1.5）
```
