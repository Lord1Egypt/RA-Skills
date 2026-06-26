# 📅 One Calendar - 单向历

每日自动发送单向历图片到飞书。

> 一天，一张图，一份日历的温度。

## ✨ 功能

- 🗓️ 根据当天日期自动获取对应图片
- 📤 通过飞书一键发送
- ⏰ 支持定时任务，每天自动发送
- 🔧 配置向导，一次设置永久使用

## 🚀 快速开始

### 1. 安装

```bash
# 从 clawhub 安装（推荐）
clawhub install one-calendar

# 或手动克隆
git clone https://github.com/chempeng/one-calendar.git ~/.openclaw/workspace/skills/one-calendar
```

### 2. 配置

```bash
cd ~/.openclaw/workspace/skills/one-calendar
node scripts/setup.js
```

向导会引导你输入飞书用户 ID、保存配置并可选发送测试。

### 3. 使用

```bash
# 手动发送
node scripts/send.js

# 在对话中触发
# 说 "单向历" / "今日单向历" / "发单向历"

# 配置定时任务（每天早上 8 点）
openclaw cron add \
  --name "每日单向历" \
  --at "0 8 * * *" \
  --session isolated \
  --message "node ~/.openclaw/workspace/skills/one-calendar/scripts/send.js" \
  --workdir ~/.openclaw/workspace
```

## 📋 配置

配置文件 `config.json`（由 `setup.js` 自动生成）：

```json
{
  "feishu": {
    "userId": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "settings": {
    "timezone": "Asia/Shanghai",
    "baseUrl": "https://img.owspace.com/Public/uploads/Download"
  }
}
```

### 获取飞书用户 ID

```bash
# 1. 启动日志监控
openclaw logs --follow

# 2. 在飞书中给机器人发送任意消息

# 3. 日志中找到 ou_xxx... 即为你的 ID
# 示例：feishu[default]: received message from ou_xxxxx...
```

### 自定义图片源

修改 `config.json` 中的 `baseUrl`，图片命名规则：`{YEAR}/{MMDD}.jpg`（如 `2026/0305.jpg`）。

## 📁 项目结构

```
one-calendar/
├── config.example.json   # 配置模板
├── config.json           # 用户配置（自动生成，已 gitignore）
├── SKILL.md              # OpenClaw 技能定义
├── README.md             # 本文件
└── scripts/
    ├── send.js           # 发送脚本
    └── setup.js          # 配置向导
```

## ❓ 常见问题

| 问题 | 解决方案 |
|------|----------|
| 配置文件不存在 | 运行 `node scripts/setup.js` |
| 用户 ID 无效 | 确认以 `ou_` 开头，重新配置 |
| 发送失败 | 检查用户 ID、飞书渠道配置、OpenClaw 状态 |
| 图片链接失效 | 确认日期格式正确，检查官方服务器状态 |

## 📝 版本历史

- **v1.1.0** (2026-03-05): 添加配置向导，支持配置文件，完善文档
- **v1.0.0** (2026-03-05): 初始版本

## 📄 许可证

MIT License

## 🙏 致谢

- [单向历官方](https://www.owspace.com/)
- [OpenClaw 社区](https://clawhub.ai/)

---

**作者**：chempeng · [GitHub](https://github.com/chempeng/one-calendar) · [Issues](https://github.com/chempeng/one-calendar/issues)
