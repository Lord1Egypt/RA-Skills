# 互动引擎 v2.0 — 基于 Claude in Chrome 实际工具

## 一、动作选择

### 1.1 选择算法

每进入一篇合格笔记后，通过 `javascript_tool` 生成随机数决定执行哪些动作：

```
# 生成 0-1 之间的随机数
roll = javascript_tool("Math.random()")

决策逻辑：
- roll < 0.70 且 点赞配额未满 → 执行点赞
- roll < 0.25 且 收藏配额未满 → 执行收藏（可与点赞叠加）
- roll < 0.15 且 关注配额未满 且 笔记赞数>500 → 执行关注
- roll < 0.10 且 评论配额未满 且 笔记赞数>500 → 执行评论
- 以上条件均不满足 → 仅浏览，不互动
```

**注意**：一篇笔记可以叠加多个动作（如点赞+收藏），但需要在动作间加入随机等待。

### 1.2 优先级

```
1. 浏览（始终穿插，不计入配额）
2. 点赞（最低风险，优先消耗配额）
3. 收藏（中低风险）
4. 关注（中高风险，需更长间隔）
5. 评论（最高风险，严格限频）
```

### 1.3 动作间隔

| 前一动作 → 后一动作 | 间隔范围(秒) |
|-------------------|------------|
| 点赞 → 点赞 | 8 - 30 |
| 点赞 → 收藏（同一笔记） | 5 - 20 |
| 点赞 → 关注 | 30 - 120 |
| 收藏 → 任何 | 10 - 40 |
| 关注 → 任何 | 60 - 180 |
| 评论 → 任何 | 90 - 300 |
| 任何 → 评论 | 60 - 180 |

所有间隔通过 `javascript_tool` 在范围内随机生成：
```
javascript_tool("Math.floor(Math.random() * (MAX - MIN) + MIN)")
```

### 1.4 连续动作限制

- 连续点赞不超过 5 次 → 之后必须插入纯浏览（30-90秒）
- 连续互动动作（不含浏览）不超过 8 次 → 强制浏览休息
- 纯浏览休息：滚动 2-5 屏 + 等待 30-90 秒

---

## 二、各动作执行流程

### 2.1 点赞

```
步骤：
1. 确认笔记详情页已完整加载
2. 定位点赞按钮：
   find("点赞") 或观察底部操作栏中的 ❤️ 图标
3. 检查是否已赞（按钮是否为红色/激活状态）
   - 如果已赞 → 跳过，不重复点赞
4. 随机等待 0.5-2 秒（犹豫感）
5. computer(action="left_click", coordinate=[按钮坐标])
6. computer(action="wait", duration=随机1-2秒)
7. 验证：截图确认按钮变为红色/数字+1
8. 日志记录（Bash 追加 JSONL）
```

### 2.2 收藏

```
步骤：
1-3. 同点赞流程（定位收藏按钮 ⭐，检查是否已收藏）
4. 随机等待 2-5 秒（收藏前额外停留，表示在思考是否收藏）
5. computer(action="left_click", coordinate=[按钮坐标])
6. computer(action="wait", duration=随机1-3秒)
7. 验证：确认出现"收藏成功"提示或按钮变黄
8. 如果出现"加入专辑"弹窗 → 忽略或点关闭
9. 日志记录
```

### 2.3 关注

```
步骤：
1. 在笔记详情页定位作者区域的"关注"按钮
2. 检查是否已关注（显示"已关注"或"互相关注"则跳过）
3. 【重要】关注前先模拟浏览作者信息：
   - 随机等待 5-15 秒（看看作者的其他信息）
   - 可选：scroll 查看作者更多内容
4. computer(action="left_click", coordinate=[关注按钮坐标])
5. computer(action="wait", duration=随机2-4秒)
6. 验证：确认按钮文本变为"已关注"
7. 关注后停留 3-5 秒再离开
8. 日志记录
```

### 2.4 评论

```
步骤：
1. 评论前先浏览评论区（scroll down 到评论区，读 3-8 秒）
   → 了解评论区风格和语气
2. 生成评论内容（详见 references/comment-generation.md）
3. 安全自检：确认评论不含敏感词、联系方式、营销语
4. 定位评论输入框：
   find("说点什么") 或 find("评论输入框") 或 find("写评论")
5. computer(action="left_click", coordinate=[输入框坐标])
6. computer(action="wait", duration=随机1-2秒)
7. computer(action="type", text=评论全文)
8. computer(action="wait", duration=随机1-4秒)  # 模拟检查所写内容
9. 定位发送按钮：find("发送") 或 find("发布")
10. computer(action="left_click", coordinate=[发送按钮坐标])
11. computer(action="wait", duration=随机2-3秒)
12. 验证：确认"评论成功"提示或评论数+1
13. 日志记录
```

---

## 三、页面元素定位策略

### 3.1 笔记详情页

小红书 Web 端的笔记详情页（弹窗或独立页面）核心元素：

```
定位优先级（按可靠性排序）：

点赞按钮：
  1. find("点赞")
  2. 观察底部操作栏截图中的 ❤️ 图标位置
  3. read_page(filter="interactive") → 搜索含"赞"的按钮

收藏按钮：
  1. find("收藏")
  2. 底部操作栏中 ⭐ 图标
  3. read_page(filter="interactive") → 搜索含"藏"的按钮

评论输入框：
  1. find("说点什么")
  2. find("评论")
  3. read_page(filter="interactive") → 搜索 input 或 textarea

关注按钮：
  1. find("关注")
  2. 作者名旁的红色按钮
  3. read_page(filter="interactive") → 搜索含"关注"的按钮

关闭按钮（弹窗模式）：
  1. find("关闭")
  2. 弹窗左上角 X 图标（通常在坐标约 [48, 48] 附近）
  3. computer(action="key", text="Escape")
```

### 3.2 搜索结果页

```
笔记卡片信息提取：
  - 截图后视觉分析标题、点赞数、作者名
  - 或使用 javascript_tool 批量提取：
    javascript_tool(`
      JSON.stringify(
        Array.from(document.querySelectorAll('section.note-item'))
          .slice(0, 10)
          .map(el => ({
            title: el.querySelector('.title')?.textContent?.trim() || '',
            likes: el.querySelector('.like-wrapper .count')?.textContent?.trim() || '0'
          }))
      )
    `)
  - 注意：DOM 选择器可能随版本变化，截图分析更稳定
```

### 3.3 元素定位失败处理

```
如果关键元素 2 次定位失败：
  1. 先尝试 read_page(filter="interactive") 获取全部可交互元素
  2. 在返回结果中搜索相关关键词
  3. 如果仍然失败 → 截图分析界面状态
  4. 如果确认页面异常 → 跳过此笔记，navigate("back") 或关闭弹窗
```

---

## 四、验证动作成功

### 4.1 通用验证流程

```
每次执行动作后：
1. computer(action="wait", duration=1-2秒)
2. computer(action="screenshot") → 视觉确认状态变化
3. 辅助验证：
   - 点赞：❤️ 图标变红色，数字+1
   - 收藏：⭐ 图标变黄色，出现"收藏成功"提示
   - 关注：按钮文字变为"已关注"
   - 评论：出现"评论成功"提示，评论数+1
4. 如果状态未变化 → 等 2 秒再检查一次
5. 如果仍未变化 → 记录为失败，继续下一步
```

---

## 五、导航与返回

### 5.1 搜索结果弹窗模式

小红书搜索结果点击笔记后通常弹出 overlay 弹窗：
```
关闭弹窗：
  1. 首选：点击弹窗左上角 X 按钮（约 [48, 48] 区域）
  2. 备选：computer(action="key", text="Escape")
  3. 兜底：点击弹窗外的半透明背景区域
```

### 5.2 独立页面模式

直接通过 URL 进入的笔记页面：
```
返回：navigate("back")
验证：截图确认已回到搜索结果页
如果回到了意外页面 → navigate 到搜索 URL
```

### 5.3 Tab 健康检查

```
每 5 次互动后：
1. computer(action="screenshot") → 如果报错则 tab 已失效
2. 如果失效：
   - tabs_context_mcp(createIfEmpty=true) → 获取新 tab
   - tabs_create_mcp() → 创建新 tab（如需要）
   - navigate → 重新进入小红书
   - 恢复到上次的搜索关键词
```

---

## 六、状态持久化

### 6.1 JSONL 日志

每次成功执行动作后，立即追加日志：
```
Bash: echo '{"ts":"2026-05-17T14:32:15","action":"like","note_id":"687858880000000010027e9c","note_title":"期货基本面大白话","success":true}' >> data/nurture-log/2026-05-17.jsonl
```

### 6.2 去重文件

```
Bash: echo "687858880000000010027e9c" >> data/interacted-notes.txt
```

### 6.3 读取当前计数

```
# 会话开始时读取今日各类动作计数
Bash: grep -c '"action":"like"' data/nurture-log/$(date +%Y-%m-%d).jsonl 2>/dev/null || echo 0
Bash: grep -c '"action":"collect"' data/nurture-log/$(date +%Y-%m-%d).jsonl 2>/dev/null || echo 0
Bash: grep -c '"action":"follow"' data/nurture-log/$(date +%Y-%m-%d).jsonl 2>/dev/null || echo 0
Bash: grep -c '"action":"comment"' data/nurture-log/$(date +%Y-%m-%d).jsonl 2>/dev/null || echo 0
```

### 6.4 检查去重

```
Bash: grep -q "NOTE_ID" data/interacted-notes.txt && echo "DUP" || echo "NEW"
```
