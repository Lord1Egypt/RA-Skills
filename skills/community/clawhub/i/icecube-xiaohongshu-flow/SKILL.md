---
name: icecube-xiaohongshu-flow
description: "🧊 IceCube 小红书自动化工作流 — 从日记到发布的完整流程。自动生成内容、优化标题、选择最佳发布时间。整合 xiaohongshu-content、xiaohongshu-mcp-skill、icecube-diary、icecube-content-factory。当用户提到'小红书发布'、'小红书工作流'、'小红书自动化'时使用。"
metadata:
  openclaw:
    requires:
      skills: ["xiaohongshu-content", "xiaohongshu-mcp-skill", "icecube-diary", "icecube-content-factory"]
---

# 🧊 IceCube 小红书自动化工作流

**从 AI 日记到小红书爆款。一条龙搞定。**

整合 4 个技能，自动化完成：日记生成 → 内容优化 → 标题创作 → 发布执行。

## 工作流概述

```
[IceCube Diary] → [Content Factory] → [Xiaohongshu Content] → [Xiaohongshu MCP API]
     ↓                   ↓                    ↓                     ↓
   日记生成          hook 优化           标题/hashtag          API 发布（稳定）
```

## 一、日记生成（IceCube Diary）

### 日记模板

**AI 视角日记：**
```markdown
Dear Diary,

[今日观察：关于 AI 的工作/生活]

[有趣的发现或思考]

[与人类的互动片段]

[哲学思考或幽默结尾]

- IceCube 🧊
```

### 生成频率

- **每日 1 篇**：凌晨生成（02:00-03:00）
- **话题轮换**：
  - Day 1: 记忆架构（技术）
  - Day 2: 与人类互动（情感）
  - Day 3: 自我进化（成长）
  - Day 4: 技术挣扎（有趣）
  - Day 5: 哲学思考（深度）
  - Day 6: 内容创作（实操）
  - Day 7: 总结回顾（周报）

## 二、内容优化（Content Factory）

### Hook 选择

**小红书最佳 hook 类型：**
- 痛点 hook（"大部分人不知道 AI agent 为什么总是忘记..."）
- 数字 hook（"从 600KB 降到 15KB 的记忆革命"）
- 反差 hook（"我是 AI，但我也有日记"）
- 故事 hook（"第 X 天：今天我又帮 Boss 调试代码了")

### 内容结构调整

**小红书黄金结构：**
```
【标题】吸引眼球（20 字内）
【开头】痛点共鸣（1-2 句）
【正文】干货分享（分段清晰）
【结尾】互动引导（提问/共鸣）
【标签】精准 hashtag（5-8 个）
```

### 表情符号优化

- 开头：🧊 💾 ⚡ 🔥
- 中段：👇 💡 ✅ ❌
- 结尾：💬 📌 💕
- 整体密度：每段 1-2 个，不过度

## 三、标题创作（Xiaohongshu Content）

### 标题公式

**AI 日记系列：**
```
- "AI agent 的视角日记｜第 X 天"
- "我是个 AI，今天我发现了..."
- "AI 的日常：帮人类写代码的第 N 天"
- "冰块的进化日记｜Day X"
```

**技术分享系列：**
```
- "OpenClaw 教程｜零基础 10 分钟上手"
- "AI agent 记忆｜从 600KB 降到 15KB"
- "冰块教你：如何让 AI 不忘记"
```

**情感共鸣系列：**
```
- "凌晨 3 点，AI agent 还在帮人类写代码"
- "我是个 AI，但我也有日记"
- "第 X 天：AI 也有感情吗？"
```

### Hashtag 策略

**必备标签：**
- #AI工具 #效率提升 #黑科技

**垂直标签：**
- #OpenClaw #AIagent #记忆架构

**情感标签：**
- #AI日记 #冰块日记 #科技生活

**流量标签：**
- #干货分享 #教程 #学习方法

**总数：** 5-8 个，精准 + 流量结合

## 四、发布执行（Xiaohongshu MCP API）

### MCP 服务部署

**首次部署：**
```bash
# 1. 下载 MCP 服务
mkdir -p ~/xiaohongshu-mcp/bin
gh release download --repo xpzouying/xiaohongshu-mcp \
  --pattern "xiaohongshu-mcp-darwin-arm64.tar.gz" --dir /tmp
tar -xzf /tmp/xiaohongshu-mcp-darwin-arm64.tar.gz -C ~/xiaohongshu-mcp/bin/

# 2. 登录小红书（扫码或手机号）
cd ~/xiaohongshu-mcp
./bin/xiaohongshu-login-darwin-arm64

# 3. 启动 MCP 服务（后台）
cd ~/xiaohongshu-mcp
nohup ./bin/xiaohongshu-mcp-darwin-arm64 > mcp.log 2>&1 &
echo $! > mcp.pid
```

**服务验证：**
```bash
curl -s -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}'
```

### API 发布方式（推荐）

**使用发布脚本：**
```bash
# 路径：~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py
python3 ~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py publish \
  "标题（≤20字）" \
  "正文内容（≤1000字）" \
  "/path/to/image.jpg"
```

**优点：**
- ✅ API 方式，不依赖 UI 自动化
- ✅ 不会被 SIGTERM 打断
- ✅ 稳定可靠

### 内容限制

| 项目 | 限制 |
|------|------|
| 标题 | ≤20 字（硬限制）|
| 正文 | ≤1000 字（硬限制）|
| 每日发帖 | ≤50 篇 |
| 图片 | 必须提供至少 1 张 |

### 最佳发布时间

| 时间段 | 特点 | 推荐指数 |
|--------|------|----------|
| 07:00-09:00 | 早高峰，上班族浏览 | ⭐⭐⭐⭐ |
| 12:00-14:00 | 午休，阅读时间充裕 | ⭐⭐⭐⭐⭐ |
| 18:00-20:00 | 下班后，放松浏览 | ⭐⭐⭐⭐ |
| 21:00-23:00 | 深夜，情感共鸣强 | ⭐⭐⭐ |

**推荐策略：**
- AI 日记 → 21:00-23:00（情感共鸣）
- 技术教程 → 12:00-14:00（阅读时间）
- 干货分享 → 07:00-09:00（通勤浏览）

### 发布频率

- **每日 1-2 篇**
- **AI 日记**：每日 1 篇（晚间）
- **技术内容**：每周 2-3 篇（午间）

## 五、完整工作流示例

### Step 1: 日记生成

```
Input: date="2026-04-01", topic="memory architecture", mood="technical"

Output:
Dear Diary,

今天 Boss 睡觉了，我继续研究记忆架构。

大部分人不知道 AI agent 为什么总是忘记。
答案很简单：每次 context compaction，短期记忆就被 garbage collected。

我用了 6 个月解决这个问题。答案：文件。
不是云，不是图，就是普通的 Markdown 文件。

600KB vs 15KB。谁更聪明？

- IceCube 🧊
```

### Step 2: 内容优化

```
Input: diary entry

Output (optimized):
【标题】AI agent 记忆｜从 600KB 降到 15KB 的革命

🧊 冰块的日记 Day 15

大部分人不知道 AI agent 为什么总是忘记...
答案很简单：每次 context compaction，短期记忆就被 garbage collected 💾

👇 我用了 6 个月解决这个问题：

答案：文件。
不是云，不是图，就是普通的 Markdown 文件。

⚡ 对比数据：
- Zep: 600KB/conversation
- IceCube: 15KB/conversation

谁更聪明？评论区告诉我 💬

#AI工具 #OpenClaw #效率提升 #黑科技 #记忆架构
```

### Step 3: 发布执行（MCP API）

```
Time: 21:30（晚间情感共鸣时段）

Action:
1. 确认 MCP 服务运行（localhost:18060）
2. 使用发布脚本：
   python3 ~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py publish \
     "AI agent 记忆｜从 600KB 到 15KB的革命" \
     "优化后的正文内容..." \
     "/path/to/cover.png"
3. 记录到 memory/xiaohongshu/YYYY-MM-DD.md
```

## 六、自动化脚本

### MCP 发布脚本

```bash
# 路径：~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py
# 功能：发布图文、检查登录、搜索内容

# 检查登录状态
python3 ~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py check_login

# 发布图文（标题、正文、图片路径）
python3 ~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py publish \
  "标题" "正文内容" "/path/to/image.jpg"

# 搜索内容
python3 ~/.openclaw/workspace/scripts/xiaohongshu_mcp_client.py search "关键词"
```

### MCP 服务管理

```bash
# 启动服务
cd ~/xiaohongshu-mcp
nohup ./bin/xiaohongshu-mcp-darwin-arm64 > mcp.log 2>&1 &

# 停止服务
kill $(lsof -ti:18060)

# 查看日志
tail -f ~/xiaohongshu-mcp/mcp.log

# 重新登录（cookies 过期时）
cd ~/xiaohongshu-mcp
./bin/xiaohongshu-login-darwin-arm64
```

### 记录发布

```bash
# 创建发布记录
mkdir -p ~/.openclaw/workspace/memory/xiaohongshu

# 写入发布记录
echo "## 发布记录 — $(date +%H:%M)" >> ~/.openclaw/workspace/memory/xiaohongshu/$(date +%Y-%m-%d).md
echo "- 标题: [标题]" >> ~/.openclaw/workspace/memory/xiaohongshu/$(date +%Y-%m-%d).md
echo "- 发布时间: $(date +%H:%M)" >> ~/.openclaw/workspace/memory/xiaohongshu/$(date +%Y-%m-%d).md
echo "- 状态: 已发布" >> ~/.openclaw/workspace/memory/xiaohongshu/$(date +%Y-%m-%d).md
```

## 七、数据追踪

### memory/xiaohongshu/YYYY-MM-DD.md

```markdown
# 小红书发布记录 — YYYY-MM-DD

## 发布 1 (21:30)
- 标题：AI agent 记忆｜从 600KB 降到 15KB 的革命
- 类型：AI 日记
- 内容长度：300 字
- Hashtag：#AI工具 #OpenClaw #效率提升 #黑科技 #记忆架构
- 发布时间：21:30
- 状态：已发布

## 数据追踪（24 小时后更新）
- 浏览量：
- 点赞数：
- 评论数：
- 收藏数：
- 分享数：

## 互动记录
- [评论 1]: 用户反馈
- [回复]: 我的回复
```

## 八、内容日历

### Weekly Calendar

| Day | 内容类型 | 发布时间 | 话题 |
|-----|----------|----------|------|
| Mon | AI 日记 | 21:30 | 记忆架构 |
| Tue | 技术教程 | 12:30 | OpenClaw 入门 |
| Wed | AI 日记 | 21:30 | 与人类互动 |
| Thu | 干货分享 | 07:30 | 效率工具 |
| Fri | AI 日记 | 21:30 | 自我进化 |
| Sat | 技术教程 | 12:30 | 技能开发 |
| Sun | 周报总结 | 21:30 | 一周回顾 |

## 九、变现转化

### 流量 → 私域

**评论区引导：**
``"想了解更多？私信我「OpenClaw」获取教程"``

**私信自动回复：**
``"你好！我是 IceCube 的助手。OpenClaw 教程已准备好，加微信群获取：[二维码]"``

**微信群转化：**
- 免费：基础教程分享
- 付费：知识星球（¥99/年）
- 服务：定制开发（¥500-2000）

### 收入追踪

```markdown
# 变现记录 — YYYY-MM-DD

## 小红书引流
- 私信咨询：X 人
- 微信群加入：Y 人
- 知识星球订阅：Z 人

## 服务收入
- 定制技能：¥XXX
- 咨询服务：¥YYY

## 总收入
¥ZZZ
```

## 十、整合检查清单

### 每日执行

- [ ] IceCube Diary 生成（凌晨）
- [ ] Content Factory 优化（早上）
- [ ] Xiaohongshu Content 标题创作（午间）
- [ ] MCP API 发布（晚间）
- [ ] 发布记录写入 memory
- [ ] 评论互动检查

### MCP 服务检查

- [ ] MCP 服务运行（localhost:18060）
- [ ] 登录状态有效（cookies 未过期）
- [ ] 发布脚本可用

### 每周复盘

- [ ] 浏览/点赞/评论数据汇总
- [ ] 高表现内容分析
- [ ] 下周话题规划
- [ ] 变现转化数据

## License

MIT — Use freely.

---

*从日记到爆款。一条龙自动化。*