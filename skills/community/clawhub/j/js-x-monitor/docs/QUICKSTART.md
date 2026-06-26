# 快速开始

## 1. 安装 Skill

```bash
# 通过 ClawHub 安装（推荐）
openclaw skill install js-x-monitor

# 或手动安装
git clone https://github.com/imjszhang/js-x-monitor-skill.git
cd js-x-monitor-skill
openclaw skill install --path .
```

## 2. 前置检查

确保以下组件已安装并运行：

```bash
# 1. 检查 OpenClaw
openclaw --version

# 2. 检查 JS-Eyes（浏览器扩展）
openclaw js-eyes status

# 3. 检查 js-search-x 技能
openclaw skill list | grep js-search-x
```

确保浏览器已登录 X.com。

## 3. 初始化

```bash
openclaw x-monitor init
```

这会创建配置文件在 `~/.openclaw/x-monitor/config.json`。

## 4. 添加监控账号

```bash
openclaw x-monitor add karpathy
openclaw x-monitor add OpenAI
openclaw x-monitor add elonmusk
```

## 5. 测试

```bash
# 测试单个账号
openclaw x-monitor test karpathy

# 查看所有监控账号
openclaw x-monitor list
```

## 6. 启动监控

```bash
openclaw x-monitor start
```

监控任务将每小时运行一次。

## 7. 查看状态

```bash
openclaw x-monitor status
```

## 8. 停止监控

```bash
openclaw x-monitor stop
```

## 配置说明

编辑 `~/.openclaw/x-monitor/config.json`：

```json
{
  "accounts": [
    {
      "username": "karpathy",
      "enabled": true
    }
  ],
  "notification": {
    "channels": ["feishu"],
    "includeRetweets": false,
    "includeReplies": false,
    "summaryLength": 100
  },
  "deduplication": {
    "method": "id_and_hash",
    "historyDays": 30
  },
  "checkInterval": 3600
}
```

## 故障排查

### Q: 测试时提示 "x_get_profile" 不存在
A: 确保 js-search-x 技能已安装：`openclaw skill install js-search-x`

### Q: 收不到通知
A: 检查消息渠道配置，确保 OpenClaw 的 channel 已正确配置

### Q: 状态文件写入失败
A: 检查目录权限：`ls -la ~/.openclaw/x-monitor/`

## 获取帮助

```bash
openclaw x-monitor --help
```

或访问 [GitHub Issues](https://github.com/imjszhang/js-x-monitor-skill/issues)
