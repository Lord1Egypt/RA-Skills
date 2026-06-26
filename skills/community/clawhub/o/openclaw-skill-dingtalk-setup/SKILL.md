---
name: dingtalk-setup
description: "钉钉企业内部机器人渠道快速对接。Use when: 用户需要对接钉钉渠道、配置钉钉 Stream 模式、排查钉钉消息问题。NOT for: 飞书/Lark、企业微信等其他平台。"
homepage: https://github.com/shaoyunhao0107/openclaw-skill-dingtalk-setup
metadata: { "openclaw": { "emoji": "💬", "requires": { "bins": ["openclaw"] } } }
---

# DingTalk Channel Setup

钉钉企业内部机器人渠道快速对接指南。

## When to Use

✅ **USE this skill when:**
- 用户说"对接钉钉"、"配置钉钉机器人"
- 钉钉消息没有响应，需要排查
- 需要安装钉钉插件
- "DingTalk channel setup"

❌ **DON'T use when:**
- 飞书/Lark 配置 → use `feishu` skill
- 企业微信 → use `wecom` skill  
- Telegram/Discord → use respective channel skills

## Prerequisites

确保已准备：
1. 钉钉开放平台企业内部应用（已创建）
2. **Client ID** (AppKey)
3. **Client Secret** (AppSecret)
4. 可选：Robot Code、Corp ID、Agent ID

## Installation

### Step 1: Install Plugin

**国内网络环境（推荐使用镜像）：**

```powershell
$env:NPM_CONFIG_REGISTRY="https://registry.npmmirror.com"
openclaw plugins install @soimy/dingtalk
```

**国际网络：**

```bash
openclaw plugins install @soimy/dingtalk
```

**如需代理：**

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
openclaw plugins install @soimy/dingtalk
```

### Step 2: Enable Plugin

编辑 `~/.openclaw/openclaw.json`，添加插件到白名单：

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["dingtalk"]
  }
}
```

如果已有其他插件，添加到数组中：

```json
{
  "plugins": {
    "allow": ["telegram", "discord", "dingtalk"]
  }
}
```

### Step 3: Configure Channel

**方式一：交互式配置（推荐）**

```bash
openclaw configure --section channels
```

按提示操作：
1. 选择 "Add a new channel"
2. 选择 "DingTalk (钉钉)"
3. 输入 Client ID
4. 输入 Client Secret
5. 选择是否配置完整信息（推荐 Yes）
6. 配置其他选项（DM/Group 策略等）
7. 完成配置

**方式二：手动编辑配置文件**

编辑 `~/.openclaw/openclaw.json`，添加 channel 配置：

```json
{
  "channels": [
    {
      "id": "dingtalk",
      "plugin": "dingtalk",
      "enabled": true,
      "clientId": "your_client_id",
      "clientSecret": "your_client_secret",
      "dm": "open",
      "group": "open"
    }
  ]
}
```

**完整配置示例：**

```json
{
  "id": "dingtalk",
  "plugin": "dingtalk",
  "enabled": true,
  "clientId": "ding3ti4ahg82dsfkwld",
  "clientSecret": "FrpMFcI30c0STvaJJWyMSZoyeb2Hkm9YqXY-6mJ0dGwdN8Xux7mgT_Xn7qnpvO-F",
  "robotCode": "your_robot_code",
  "corpId": "your_corp_id",
  "agentId": "your_agent_id",
  "aiCard": false,
  "dm": "open",
  "group": "open"
}
```

**方式三：自动化脚本（推荐批量部署）**

使用提供的 PowerShell 脚本：

```powershell
.\scripts\auto-setup.ps1 -ClientId "your_id" -ClientSecret "your_secret"
```

完整参数：

```powershell
.\scripts\auto-setup.ps1 `
    -ClientId "ding3ti4ahg82dsfkwld" `
    -ClientSecret "FrpMFcI30c0STvaJJWyMSZoyeb2Hkm9YqXY-6mJ0dGwdN8Xux7mgT_Xn7qnpvO-F" `
    -RobotCode "your_robot_code" `
    -CorpId "your_corp_id" `
    -AgentId "your_agent_id" `
    -UseProxy
```

### Step 4: Restart Gateway

```bash
openclaw gateway restart
```

## Configuration Options

| 参数 | 必需 | 说明 | 默认值 |
|------|------|------|--------|
| `clientId` | ✅ | DingTalk App Key | - |
| `clientSecret` | ✅ | DingTalk App Secret | - |
| `robotCode` | ❌ | 机器人代码 | - |
| `corpId` | ❌ | 企业 ID | - |
| `agentId` | ❌ | 应用 Agent ID | - |
| `aiCard` | ❌ | 启用 AI 互动卡片 | `false` |
| `dm` | ❌ | 私聊策略：`open` / `allowlist` | `open` |
| `group` | ❌ | 群聊策略：`open` / `allowlist` | `open` |

## Verification

测试连接：

```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看日志
openclaw logs gateway

# 列出插件
openclaw plugins list
```

在钉钉中给机器人发送消息，应该能收到回复。

## Troubleshooting

### 插件安装卡住

如果安装停在 "Installing plugin dependencies..."：

```bash
cd ~/.openclaw/extensions/dingtalk
rm -rf node_modules package-lock.json
NPM_CONFIG_REGISTRY=https://registry.npmmirror.com npm install
openclaw gateway restart
```

### 机器人无响应

检查清单：

1. ✅ **Gateway 运行中**
   ```bash
   openclaw gateway status
   ```

2. ✅ **插件在白名单**
   检查 `openclaw.json` 中的 `plugins.allow` 包含 `"dingtalk"`

3. ✅ **渠道已启用**
   检查 `channels[].enabled` 为 `true`

4. ✅ **凭证正确**
   在钉钉开放平台验证 Client ID/Secret

5. ✅ **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

### 网络问题（中国大陆）

```powershell
# 设置 npm 镜像
$env:NPM_CONFIG_REGISTRY="https://registry.npmmirror.com"

# 设置代理（如需要）
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
```

### 常见错误

**"Plugin not found"**
- 确认插件已安装：`openclaw plugins list`
- 检查目录存在：`~/.openclaw/extensions/dingtalk`

**"Connection failed"**
- 验证钉钉开放平台凭证
- 检查网络连接
- 查看日志：`openclaw logs gateway`

**"Plugin not loaded"**
- 添加 `dingtalk` 到 `plugins.allow`
- 重启 Gateway

## Files & Locations

- **配置文件**: `~/.openclaw/openclaw.json`
- **插件目录**: `~/.openclaw/extensions/dingtalk`
- **日志**: `openclaw logs gateway`
- **自动化脚本**: `scripts/auto-setup.ps1`

## References

- [插件仓库](https://github.com/soimy/openclaw-channel-dingtalk)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [钉钉开放平台](https://open.dingtalk.com)

## Notes

- 使用 Stream 模式（无需公网 IP）
- 支持私聊和群聊
- AI 互动卡片可选
- 仅支持企业内部应用
- 提供自动化部署脚本
