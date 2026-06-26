# OpenClaw 故障排除 Skill

## 症状：失忆症（无法记住对话）

### 诊断步骤
1. 检查 memory 插件状态：`openclaw plugins list | grep memory`
2. 检查会话文件：`ls ~/.openclaw/agents/main/sessions/`
3. 检查 MEMORY.md 是否存在：`ls ~/.openclaw/workspace/MEMORY.md`

### 修复方案
```bash
# 启用 memory-core 插件
openclaw plugins enable memory-core

# 添加到允许列表
jq '.plugins.allow += ["memory-core"]' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 重启 Gateway
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## 症状：飞书连接断开

### 诊断步骤
1. 检查 Gateway 状态：`openclaw gateway status`
2. 检查通道状态：`openclaw status | grep -A 5 "Channels"`
3. 查看错误日志：`tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log`

### 修复方案
```bash
# 强制重启 Gateway
killall openclaw-gateway 2>/dev/null
sleep 2
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

---

## 症状：LLM Timeout

### 注意
OpenClaw 的 config schema **不支持**直接在 providers 下加 `timeout` 字段。

### 正确做法
- 使用默认超时设置
- 如需要调整，通过环境变量或 API 调用时指定

---

## 症状：Telegram 疯狂报错

### 修复方案
```bash
# 禁用 Telegram
openclaw config set plugins.allow '["feishu"]'  # 只保留飞书
openclaw config set plugins.entries.telegram.enabled false
openclaw config set channels.telegram.enabled false

# 重启生效
openclaw gateway restart
```

---

## 配置原则

1. **插件最小化** - 只启用需要的插件
2. **配置验证** - 修改后用 `openclaw doctor` 检查
3. **备份习惯** - 重要修改前手动备份 `openclaw.json`

## 关键文件位置

- 主配置：`~/.openclaw/openclaw.json`
- 会话存储：`~/.openclaw/agents/main/sessions/`
- 长期记忆：`~/.openclaw/workspace/MEMORY.md`
- 日志文件：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 服务配置：`~/Library/LaunchAgents/ai.openclaw.gateway.plist`
