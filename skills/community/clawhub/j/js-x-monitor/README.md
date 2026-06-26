# js-x-monitor-skill

X.com (Twitter) 账号监控 Skill for OpenClaw - 自动监控指定账号动态，新推文实时推送。

## 功能特性

- 🕐 **定时监控**：每小时自动检查指定 X.com 账号
- 🔔 **实时通知**：新推文即时推送到飞书/微信/Discord
- 🧠 **智能去重**：基于推文 ID + 内容哈希双重校验
- 💰 **零成本**：相比第三方工具 ($20+/月)，本地部署几乎免费
- 🔒 **隐私安全**：数据不出本地，登录态复用你的浏览器

## 前置要求

1. **OpenClaw** 已安装并运行
2. **JS-Eyes** 浏览器扩展已安装并连接
3. **js-search-x** 扩展技能已安装
4. 你的浏览器已登录 X.com

## 安装

### 方法 1：ClawHub 安装（推荐）

```bash
openclaw skill install js-x-monitor
```

### 方法 2：手动安装

```bash
git clone https://github.com/imjszhang/js-x-monitor-skill.git
cd js-x-monitor-skill
openclaw skill install --path .
```

## 快速开始

### 1. 初始化配置

```bash
openclaw x-monitor init
```

这将创建：
- 配置文件：`~/.openclaw/x-monitor/config.json`
- 状态目录：`~/.openclaw/x-monitor/state/`

### 2. 添加监控账号

```bash
openclaw x-monitor add <username>
```

例如：
```bash
openclaw x-monitor add karpathy
openclaw x-monitor add elonmusk
openclaw x-monitor add OpenAI
```

### 3. 启动监控

```bash
openclaw x-monitor start
```

## 配置说明

配置文件 `~/.openclaw/x-monitor/config.json`：

```json
{
  "accounts": [
    {
      "username": "karpathy",
      "enabled": true,
      "checkInterval": 3600,
      "notifyChannel": "feishu"
    }
  ],
  "notification": {
    "channels": ["feishu", "weixin"],
    "includeRetweets": false,
    "includeReplies": false,
    "summaryLength": 100
  },
  "deduplication": {
    "method": "id_and_hash",
    "historyDays": 30
  }
}
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `openclaw x-monitor init` | 初始化配置 |
| `openclaw x-monitor add <user>` | 添加监控账号 |
| `openclaw x-monitor remove <user>` | 移除监控账号 |
| `openclaw x-monitor list` | 列出所有监控账号 |
| `openclaw x-monitor start` | 启动监控 |
| `openclaw x-monitor stop` | 停止监控 |
| `openclaw x-monitor status` | 查看状态 |
| `openclaw x-monitor test <user>` | 测试单个账号 |

## 技术架构

```
┌─────────────────┐
│   X.com 网站    │
└────────┬────────┘
         │
┌────────▼────────┐
│  JS-Eyes 扩展   │  ← 复用你的浏览器登录态
└────────┬────────┘
         │ WebSocket
┌────────▼────────┐
│  OpenClaw GW    │
└────────┬────────┘
         │
┌────────▼────────┐
│ x-monitor Skill │  ← 本 Skill
│   - x_get_profile
│   - 去重逻辑
│   - 通知推送
└────────┬────────┘
         │
┌────────▼────────┐
│   消息渠道      │  ← 飞书/微信/Discord
└─────────────────┘
```

## 数据存储

- **状态文件**：`~/.openclaw/x-monitor/state/<username>.json`
- **日志文件**：`~/.openclaw/x-monitor/logs/`
- **配置备份**：`~/.openclaw/x-monitor/backup/`

## 成本估算

监控 5 个账号，每小时检查一次：

| 项目 | 月消耗 |
|------|--------|
| API Token | ~$1.0 |
| 存储 | 可忽略 |
| **总计** | **~$1/月** |

对比第三方工具：$20+/月

## 故障排查

### Q: 监控任务超时
A: 检查 JS-Eyes 扩展是否已连接，浏览器是否已登录 X.com

### Q: 收不到通知
A: 检查消息渠道配置，确保 OpenClaw 的消息渠道已正确设置

### Q: 重复通知
A: 检查状态文件权限，确保 Skill 有写入权限

## 贡献

欢迎 PR！请遵循以下规范：
1. Fork 本仓库
2. 创建功能分支
3. 提交 PR 到 main 分支

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- [JS-Eyes](https://github.com/imjszhang/JS-Eyes) - 浏览器自动化
- [js-search-x](https://github.com/imjszhang/js-search-x) - X.com 搜索技能

---

Made with ❤️ by [JS](https://github.com/imjszhang)
