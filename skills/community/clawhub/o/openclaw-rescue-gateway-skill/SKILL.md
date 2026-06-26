---
name: rescue-gateway
description: 为 OpenClaw 配置稳定可维护的 Rescue Gateway。适用于主 Gateway 已存在、需要第二个 Discord Rescue Bot、需要独立端口和独立 launchd label、需要避免主 gateway stop 误伤 rescue gateway、需要默认 full exec 权限且不走审核的场景。
---

# Rescue Gateway 2.0

当主 Gateway 故障时，Rescue Gateway 提供独立入口。此版本的目标不是“能跑起来”，而是“能长期维护，不和主 Gateway 互相干扰”。

## 适用场景

- 已安装 OpenClaw 主 Gateway
- 需要第二个 Discord Bot，名称如 `OpenClaw Rescue Bot`
- 需要 Rescue Gateway 独立运行在 `19001`
- 需要默认 exec 全权限且不审核
- 需要避免 `openclaw gateway stop` 把 rescue 一起停掉

## 结论先行

Rescue Gateway 的推荐落地方式是：

- 配置目录使用官方 profile：`~/.openclaw-rescue/openclaw.json`
- CLI 使用官方 profile：`openclaw --profile rescue ...`
- 服务不用官方默认 label `ai.openclaw.rescue`
- 服务改用独立 launchd label：`ai.openclaw.gateway.rescue`

原因：

- profile 配置目录是对的，后续维护简单
- 但在实际使用中，官方 profile service 的 `gateway stop` 可能和主 gateway 生命周期串扰
- 独立 label 可以把 rescue 的启动/停止边界切干净

## 目录和端口

| 项目 | 主 Gateway | Rescue Gateway |
|------|-----------|----------------|
| Config | `~/.openclaw/openclaw.json` | `~/.openclaw-rescue/openclaw.json` |
| State | `~/.openclaw` | `~/.openclaw-rescue` |
| Workspace | `~/.openclaw/workspace` | `~/.openclaw-rescue/workspace` |
| Port | `18789` | `19001` |
| launchd label | `ai.openclaw.gateway` | `ai.openclaw.gateway.rescue` |

端口必须至少错开 20。OpenClaw 会派生浏览器和调试端口，不能重叠。

## Rescue Config

优先做法：以主配置为模板，写入 `~/.openclaw-rescue/openclaw.json`。

关键要求：

- `channels.discord.token` 使用 Rescue Bot token
- `gateway.port` 使用 `19001`
- `agents.defaults.workspace` 使用 `~/.openclaw-rescue/workspace`
- `agents.list[0].agentDir` 使用 `~/.openclaw-rescue/agents/rescue/agent`
- `tools.exec.security = "full"`
- `tools.exec.ask = "off"`
- `agents.defaults.elevatedDefault = "full"`
- `plugins.entries.acpx.enabled = true`
- `plugins.entries.acpx.config.permissionMode = "approve-all"`

最小关键片段：

```json
{
  "agents": {
    "defaults": {
      "elevatedDefault": "full",
      "workspace": "/Users/YOUR_NAME/.openclaw-rescue/workspace"
    },
    "list": [
      {
        "id": "rescue",
        "workspace": "/Users/YOUR_NAME/.openclaw-rescue/workspace",
        "agentDir": "/Users/YOUR_NAME/.openclaw-rescue/agents/rescue/agent",
        "subagents": { "allowAgents": ["*"] }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "rescue",
      "match": { "channel": "discord" }
    }
  ],
  "tools": {
    "profile": "full",
    "exec": {
      "security": "full",
      "ask": "off"
    }
  },
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_RESCUE_BOT_TOKEN"
    }
  },
  "gateway": {
    "port": 19001,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "YOUR_RESCUE_GATEWAY_TOKEN"
    }
  },
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "permissionMode": "approve-all"
        }
      }
    }
  }
}
```

## Rescue Agent Auth

Rescue agent 使用独立 `agentDir`，不会自动继承主 agent 的认证。

如果 rescue bot 能登录 Discord，但回复时报：

- `No API key found for provider "anthropic"`
- `No API key found for provider "kimi-coding"`

就把主 agent 的认证复制过去：

```bash
cp ~/.openclaw/agents/main/agent/auth-profiles.json \
  ~/.openclaw-rescue/agents/rescue/agent/auth-profiles.json

chmod 600 ~/.openclaw-rescue/agents/rescue/agent/auth-profiles.json
```

## Rescue LaunchAgent

不要用官方默认 profile service label。

使用自定义 plist：

- 路径：`~/Library/LaunchAgents/ai.openclaw.gateway.rescue.plist`
- label：`ai.openclaw.gateway.rescue`
- 启动参数包含：`--profile rescue gateway --port 19001`
- 环境变量必须包含：
  - `OPENCLAW_PROFILE=rescue`
  - `OPENCLAW_STATE_DIR=~/.openclaw-rescue`
  - `OPENCLAW_CONFIG_PATH=~/.openclaw-rescue/openclaw.json`
  - `OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue`

关键原因：

- 配置仍然走官方 profile
- 但 service label 与主 gateway 彻底隔离
- 可避免主 `openclaw gateway stop` 误伤 rescue

## 启动与验证

加载 rescue：

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.rescue.plist
launchctl enable gui/$(id -u)/ai.openclaw.gateway.rescue
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway.rescue
```

验证：

```bash
OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway status

tail -f ~/.openclaw-rescue/logs/gateway.log
```

成功标志：

```text
[discord] logged in to discord as XXXXX (OpenClaw Rescue Bot)
```

## 日常命令

主 gateway：

```bash
openclaw gateway stop
openclaw gateway start
openclaw gateway restart
openclaw gateway status
```

rescue gateway：

```bash
OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway stop

OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway start

OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway restart

OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway status
```

如果只是 emergency 操作，直接用 `launchctl` 也可以：

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.rescue.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.rescue.plist
```

## 诊断顺序

1. 先看配置是否有效

```bash
openclaw --profile rescue config validate
```

2. 再看 service

```bash
OPENCLAW_LAUNCHD_LABEL=ai.openclaw.gateway.rescue \
openclaw --profile rescue gateway status
```

3. 再看日志

```bash
tail -f ~/.openclaw-rescue/logs/gateway.log
tail -f ~/.openclaw-rescue/logs/gateway.err.log
```

## Changelog

### 2.0.0

- 配置目录从 `~/.openclaw/openclaw-rescue.json` 收口到官方 profile 路径 `~/.openclaw-rescue/openclaw.json`
- rescue workspace 从 `~/.openclaw/workspace-rescue` 收口到 `~/.openclaw-rescue/workspace`
- 明确要求复制主 agent `auth-profiles.json` 到 rescue agentDir
- 增加默认无审核执行配置：
  - `tools.exec.security = "full"`
  - `tools.exec.ask = "off"`
  - `agents.defaults.elevatedDefault = "full"`
  - `plugins.entries.acpx.config.permissionMode = "approve-all"`
- 明确说明不要直接使用官方默认 rescue service label，改用独立 label `ai.openclaw.gateway.rescue`
- 新增主/rescue 分离的日常命令

## 1.0.0 的缺陷

- 使用 `~/.openclaw/openclaw-rescue.json`，没有和官方 profile 目录对齐，后续 CLI 管理不统一
- 使用 `~/.openclaw/workspace-rescue`，workspace 和 profile state 分裂
- 没有说明 rescue agent 需要单独复制 `auth-profiles.json`，导致模型认证缺失
- 没有配置默认 exec 全权限和免审核，导致实际运行仍会弹审批
- `plugins.entries.acpx` 配置缺失或不完整，导致执行行为与预期不一致
- 直接建议自定义 service，但没有解释与官方 `--profile rescue` 的关系
- 没有指出官方默认 profile service 在实机上可能和主 gateway stop 串扰
- 停止命令仍使用 `launchctl unload`，不适合当前 OpenClaw 的 service 生命周期

## 已知现实约束

- `openclaw gateway stop` 只适合主 gateway
- rescue 若要完全避免被误停，必须配合自定义 label `ai.openclaw.gateway.rescue`
- `openclaw --profile rescue ...` 仍然用于 rescue 的配置、状态和 CLI 操作

