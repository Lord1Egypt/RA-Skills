# 反检测策略 v2.0 — 基于 Claude in Chrome 实际能力

## 核心原则

1. **所有操作在用户可见的 Chrome 窗口中执行** — 不使用 Headless 模式
2. **不修改浏览器指纹** — 不注入 Canvas/WebGL/UA 伪装
3. **不调用平台私有 API** — 仅通过 DOM 交互
4. **行为模式接近真人统计分布** — 不追求效率，追求自然
5. **最大化可控维度的随机性** — 弥补不可控维度的局限

## 工具能力边界（必须理解）

Claude in Chrome 的 `computer` 工具限制：
- `left_click(coordinate)` — 瞬移+点击，**无鼠标移动轨迹**
- `type(text)` — 一次性输入完整字符串，**无法逐字控制间隔**
- `scroll(direction, amount)` — 整数档位滚动
- `wait(duration)` — 秒级精度等待
- `hover(coordinate)` — 移动鼠标到坐标（不点击）

**不可实现的功能**（已从设计中移除）：
- 贝塞尔曲线鼠标移动路径
- 逐字符输入 + 毫秒级间隔
- 模拟打字错误并退格
- 亚秒级精确时间控制

因此，**所有反检测努力集中在以下可控维度**。

---

## 一、随机等待时间（最关键的反检测手段）

### 1.1 生成随机数

所有随机数通过 `javascript_tool` 在浏览器中生成，确保真正的随机性：

**均匀分布**（用于大多数等待场景）：
```
javascript_tool("Math.floor(Math.random() * (MAX - MIN) + MIN)")
```

**高斯分布**（用于阅读时间、打字前停顿等更自然的场景）：
```
javascript_tool(`
  var base = BASE_VALUE;
  var std = base * 0.3;
  var u1 = Math.random(), u2 = Math.random();
  var z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  Math.max(Math.floor(base + z * std), Math.floor(base * 0.3))
`)
```

### 1.2 规则：永远不使用固定时间

**错误做法**（会被检测为机器人）：
```
wait(duration=3)  # 每次都是3秒
wait(duration=5)  # 每次都是5秒
```

**正确做法**：
```
# 先生成随机时间
random_seconds = javascript_tool("Math.floor(Math.random() * 5 + 2)")
# 再执行等待
wait(duration=random_seconds)
```

### 1.3 各场景等待时间范围

| 场景 | 最小(秒) | 最大(秒) | 分布 |
|------|---------|---------|------|
| 页面加载后 | 1 | 3 | 均匀 |
| 阅读笔记标题区 | 2 | 6 | 高斯(μ=4) |
| 查看图片（每张） | 1.5 | 4 | 均匀 |
| 阅读正文（每100字） | 3 | 8 | 高斯(μ=5) |
| 查看评论区 | 3 | 12 | 高斯(μ=6) |
| 点赞前犹豫 | 0.5 | 2 | 均匀 |
| 点赞后停留 | 1 | 3 | 均匀 |
| 收藏前额外停留 | 2 | 5 | 均匀 |
| 评论前思考 | 3 | 8 | 高斯(μ=5) |
| 评论输入后检查 | 1 | 4 | 均匀 |
| 关注前浏览作者 | 5 | 15 | 高斯(μ=8) |
| 关闭笔记前 | 1 | 4 | 均匀 |
| 搜索结果间浏览 | 2 | 6 | 均匀 |
| 换关键词间隔 | 5 | 15 | 均匀 |

---

## 二、滚动行为随机化

### 2.1 变量化滚动参数

每次滚动的 `scroll_amount` 都不同：
```
random_amount = javascript_tool("Math.floor(Math.random() * 4 + 2)")
# 结果 2-5，不要固定为 3
computer(action="scroll", direction="down", scroll_amount=random_amount)
```

### 2.2 回滚行为（模拟"回头看"）

真人经常在滚动后回头看之前的内容。每次滚动后生成概率判断：
```
should_back = javascript_tool("Math.random() < 0.12 ? 'yes' : 'no'")
if should_back == "yes":
    wait(random 1-3秒)
    computer(action="scroll", direction="up", scroll_amount=1或2)
    wait(random 2-5秒)
```

### 2.3 分段式滚动（不一次滚到底）

浏览长笔记时，将滚动分成多段：
```
总需滚动量 = 6
第一段: scroll(down, 2) → wait(3-6秒，阅读)
第二段: scroll(down, 2) → wait(4-8秒，阅读)
第三段: scroll(down, 2) → wait(2-4秒)
偶尔插入: scroll(up, 1) → wait(2-3秒) → scroll(down, 2) → wait(3-5秒)
```

### 2.4 变速滚动模式

不同时间段的滚动速度不同：
- 刚进入页面：滚动慢，停留久（好奇）
- 中段浏览：滚动较快（扫读）
- 发现感兴趣内容：突然减速，停留变长
- 评论区：慢速逐条浏览

---

## 三、笔记选择的不可预测性

### 3.1 不要总选第一个合格笔记

从符合条件的笔记中随机选择，而非按顺序选第一个：
```
# 收集当前可见的合格笔记列表
qualifying_notes = [分析可见笔记中符合过滤条件的]
if len(qualifying_notes) > 1:
    random_index = javascript_tool(f"Math.floor(Math.random() * {len(qualifying_notes)})")
    选择 qualifying_notes[random_index]
```

### 3.2 故意跳过合格笔记（20%概率）

真人不会对每个好内容都互动。有时候会"滑过去"：
```
skip_this = javascript_tool("Math.random() < 0.20 ? 'skip' : 'interact'")
if skip_this == "skip":
    # 仅浏览，不互动，继续滚动
```

### 3.3 偶尔与非目标内容互动（5%概率）

人的好奇心会让他们点开与目标无关的内容：
```
curiosity = javascript_tool("Math.random() < 0.05 ? 'yes' : 'no'")
if curiosity == "yes":
    # 点开一个不在目标关键词范围内的笔记
    # 浏览几秒后返回（不执行点赞等操作）
```

### 3.4 模拟误点击（3%概率）

真人偶尔会误点笔记然后立刻退出：
```
misclick = javascript_tool("Math.random() < 0.03 ? 'yes' : 'no'")
if misclick == "yes":
    # 点击一个随机笔记
    wait(0.5-1秒)
    # 立刻关闭/返回
```

---

## 四、会话节奏曲线

### 4.1 不均匀的操作分布

真人的活跃度在会话中呈现自然曲线，不是匀速的：

| 会话阶段 | 占比 | 间隔倍数 | 行为特征 |
|---------|------|---------|---------|
| 预热（开头） | 0-10% | ×2.0 | 纯浏览，不互动 |
| 渐入状态 | 10-25% | ×1.5 | 开始互动，但频率较低 |
| 活跃期 | 25-75% | ×1.0 | 正常频率互动 |
| 疲劳期 | 75-90% | ×1.3 | 频率降低，浏览增多 |
| 收尾期 | 90-100% | ×2.5 | 很少互动，纯浏览，准备离开 |

实现方式：
```
# 在每个动作前计算当前所在阶段
elapsed_ratio = (当前时间 - 开始时间) / 计划总时长

if elapsed_ratio < 0.10:
    interval_multiplier = 2.0
elif elapsed_ratio < 0.25:
    interval_multiplier = 1.5
elif elapsed_ratio < 0.75:
    interval_multiplier = 1.0
elif elapsed_ratio < 0.90:
    interval_multiplier = 1.3
else:
    interval_multiplier = 2.5

实际间隔 = 基准间隔 × interval_multiplier × random_jitter
```

### 4.2 动作类型的自然穿插

不要连续做同类动作（如连续5个点赞）。穿插浏览行为：

```
每执行 2-4 个互动动作（随机）后：
  → 插入 1 次"纯浏览"（滚动 2-3 屏，不点击任何按钮）
  → 持续 15-45 秒（随机）

连续点赞不超过 config.jitter.max_consecutive_likes 次
连续动作（不含浏览）不超过 config.jitter.max_consecutive_actions 次
```

### 4.3 会话起始行为变化

不要每次都以相同方式开始会话。随机选择起始路径：
```
start_mode = javascript_tool("Math.floor(Math.random() * 3)")
if start_mode == 0:
    → 先浏览首页推荐流 → 再搜索
elif start_mode == 1:
    → 直接搜索第一个关键词
else:
    → 先看通知/消息 → 回首页 → 再搜索
```

---

## 五、环境一致性红线

以下操作**绝对禁止**，会直接触发小红书风控：

1. **不修改 User-Agent** — 保持浏览器原始 UA
2. **不修改 Canvas/WebGL 指纹** — 不注入 Canvas 随机化脚本
3. **不使用 CDP（Chrome DevTools Protocol）** — 不直接操控 Chrome
4. **不拦截/修改 XHR/Fetch 请求** — 不对小红书 API 做任何操作
5. **不操作 Cookie/localStorage** — 不手动修改认证信息
6. **不使用自动化标识** — 不设置 `navigator.webdriver = true`
7. **不进行短时间内的高频操作** — 严格遵循速率控制

---

## 六、风控信号检测

每次动作后必须检查页面是否出现异常信号：

### 6.1 检测方法

```
# 方法1：find 搜索关键词
find("验证码") → 如果找到 = 触发验证码
find("滑块") → 如果找到 = 滑块验证
find("操作频繁") → 如果找到 = 频率警告
find("异常") → 如果找到 = 账号异常
find("违规") → 如果找到 = 违规提示
find("登录") → 如果在非登录页找到 = 登录失效

# 方法2：read_page 扫描
read_page(filter="all", depth=3) → 在返回文本中搜索风控关键词
```

### 6.2 响应矩阵

| 信号 | 级别 | 响应 |
|------|------|------|
| 按钮无响应 | Low | wait 30秒 → 重试 ×2 → 跳过 |
| "操作频繁" 提示 | Medium | **立即暂停 5-10 分钟**，纯浏览 |
| Toast 警告弹窗 | Medium | 暂停 10 分钟，降低后续频率 |
| 滑块/图形验证码 | High | **立即停止**，通知用户手动处理 |
| 登录失效 | Critical | 终止会话，保存状态，通知用户 |
| 违规提示 | Critical | **立即终止**，建议 24h 不操作 |

### 6.3 累积风控

```
同一会话内：
- 出现 1 次 Medium 信号 → 所有间隔翻倍
- 出现 2 次 Medium 信号 → 暂停 15 分钟
- 出现 3 次 Medium 信号 → 终止会话
- 出现任何 High/Critical 信号 → 立即终止
```

---

## 七、阅读行为模拟

### 7.1 图文笔记

```
1. 进入笔记 → wait(随机 2-5秒，看首图)
2. 图片浏览：
   - 检测图片数量（看翻页指示器）
   - 每张图：scroll(down, 1-2) → wait(随机 1.5-4秒)
   - 不一定看完所有图（随机看 60-100%）
3. 文字阅读：
   - scroll(down, 2-3) 进入文字区
   - 按内容长度停留：每100字约 3-8秒（高斯分布）
   - 长文阅读中插入 1-2 次停顿（模拟思考）
4. 评论区浏览（50%概率）：
   - scroll(down, 2-3) 到评论区
   - wait(随机 3-10秒)
   - 浏览 1-3 条热评
```

### 7.2 视频笔记

```
1. 进入笔记 → 视频自动播放
2. 观看时长 = 视频时长 × random(0.4, 1.0)
3. wait(观看时长)
4. 30%概率拉到评论区看评论
```

### 7.3 搜索结果页浏览

```
1. 搜索完成后 → wait(随机 2-4秒，扫视结果)
2. 每滚动一屏 → wait(随机 3-6秒，扫视卡片)
3. 看到感兴趣的卡片 → 可能多停留 1-2秒
4. 有时回滚看之前的结果
```
