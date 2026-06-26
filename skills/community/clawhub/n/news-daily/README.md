# 新闻日报 (News Daily)

获取每日新闻热榜并发送到飞书群。支持国内、国际、科技、AI 四个分类。

## 功能特点

- 📰 **多源 RSS 聚合** - 自动获取多个 RSS 源
- 🎨 **飞书卡片格式** - 美观的卡片消息，带可点击链接
- ⚙️ **可配置** - 支持自定义新闻分类和数量
- 🤖 **定时自动发送** - 可配置定时任务

## 快速开始

### 1. 安装

```bash
# 克隆或下载此技能到你的 OpenClaw workspace
cp -r news-daily ~/.openclaw/workspace/skills/
```

### 2. 配置 Webhook

你需要配置一个飞书机器人 Webhook：

**创建飞书机器人：**
1. 打开飞书群设置 → 群机器人 → 添加机器人
2. 选择 "自定义机器人"
3. 设置机器人名称（如 "新闻日报"）
4. 复制 Webhook 地址

**配置方式（选择一种）：**

方式一：环境变量（推荐）
```bash
export NEWS_DAILY_WEBHOOK="你的飞书Webhook地址"
```

方式二：配置文件
```bash
# 编辑 config.json
vim ~/.openclaw/workspace/skills/news-daily/scripts/config.json
```

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx",
  "date": "today",
  "categories": {
    "国内": 10,
    "国际": 10,
    "科技": 10,
    "AI": 10
  }
}
```

### 3. 手动发送测试

```bash
python3 ~/.openclaw/workspace/skills/news-daily/scripts/fetch_and_send.py
```

### 4. 配置定时任务

使用 OpenClaw cron：

```bash
# 添加每日 8 点定时任务
openclaw cron add --name "新闻日报" --cron "0 8 * * *" --system-event "news-daily" --session main
```

或者使用 OpenClaw hooks：

```bash
openclaw config set hooks.internal.entries.news-daily.enabled true
openclaw config set hooks.internal.entries.news-daily.systemEvent "news-daily"
openclaw config set hooks.internal.entries.news-daily.action.kind "exec"
openclaw config set hooks.internal.entries.news-daily.action.command "python3 ~/.openclaw/workspace/skills/news-daily/scripts/fetch_and_send.py"
openclaw gateway restart
```

## 配置说明

### config.json 完整配置

```json
{
  "webhook_url": "飞书机器人 Webhook 地址",
  "date": "today",  // 或 yesterday，或具体日期 YYYY-MM-DD
  "categories": {
    "国内": 10,
    "国际": 10,
    "科技": 10,
    "AI": 10
  }
}
```

### RSS 源

- **国内**：中国新闻网、人民日报
- **国际**：纽约时报、BBC、卫报
- **科技**：36氪、少数派、TechCrunch、The Verge
- **AI**：InfoQ、机器之心、MIT 科技评论、VentureBeat

## 输出格式

默认输出为飞书卡片格式，示例：

```
📰 新闻热榜 - 2026-03-07

📰 国内新闻 (10条)
1. [标题](链接)
2. [标题](链接)
...

🌍 国外新闻 (10条)
...

💻 科技新闻 (10条)
...

🤖 AI新闻 (10条)
...
```

## 常见问题

**Q: 消息发送失败？**
A: 检查 Webhook 地址是否正确，确保机器人已添加到群聊。

**Q: 如何修改发送时间？**
A: 修改 cron 表达式，如 `0 9 * * *` 为每天 9 点。

**Q: 如何只获取特定分类？**
A: 修改 config.json 中的 categories 配置。

## 开源许可

MIT License
