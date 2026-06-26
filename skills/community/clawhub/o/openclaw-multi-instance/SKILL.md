---
name: openclaw-multi-instance
description: "OpenClaw 多实例互联。当用户有多台机器运行 OpenClaw，想让它们互相通信、传文件、共享记忆时使用。触发词：多实例、互联、另一台服务器、同步记忆、实例通信。"
---

# OpenClaw 多实例互联

让多台机器上的 OpenClaw 实例互相通信、传文件、共享记忆，实现无感切换。

## 什么时候用这个 Skill

- 用户说"我还有一台服务器也跑了 OpenClaw"
- 用户想从一台 OpenClaw 操控另一台
- 用户想让多台实例共享记忆/身份
- 用户提到多实例互联、同步等需求

## 架构概览

```
┌──────────────────┐         ┌──────────────────┐
│   实例 A (本地)    │         │   实例 B (远程)    │
│                  │  SSH    │                  │
│  OpenClaw    ────┼────────▶│  OpenClaw         │
│                  │  API    │                  │
└──────────────────┘         └──────────────────┘
        │                            │
        └──── 定期对账（记忆叠加合并） ──┘
```

三种能力：
1. **API 通信** — 实例之间直接对话
2. **SSH 传文件** — 免密传输任意大小文件
3. **记忆同步** — 定期合并记忆，不覆盖，只叠加

## 搭建流程

### Step 1: 开启远程实例的 API Endpoint

远程实例需要在配置中开启 Chat Completions endpoint：

```json5
// ~/.openclaw/openclaw.json
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}
```

然后重启 Gateway：`openclaw gateway restart`

**验证**：用 curl 测试：
```bash
curl -sS http://<远程IP>:<端口>/v1/chat/completions \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{"model":"openclaw:main","messages":[{"role":"user","content":"ping"}]}'
```

**获取 Token**：查看远程实例的 `gateway.auth.token` 或环境变量 `OPENCLAW_GATEWAY_TOKEN`。

### Step 2: 配置 SSH 免密登录

**如果本地有公钥**，直接让远程实例帮忙加：

```
通过 API 告诉远程实例：
"请把以下公钥加到 authorized_keys：
<本地 cat ~/.ssh/id_ed25519.pub 的内容>
追加到 ~/.ssh/authorized_keys，chmod 600"
```

**如果远程有公钥**，本地加：
```bash
# 获取远程公钥（通过 API 问远程实例要）
# 然后本地：
echo "<公钥内容>" >> ~/.ssh/authorized_keys
```

**测试**：`ssh <用户>@<远程IP> "echo OK"`

### Step 3: 同步核心文件

通过 scp 把身份和记忆同步过去：

```bash
scp IDENTITY.md SOUL.md USER.md MEMORY.md TOOLS.md AGENTS.md \
    <用户>@<远程IP>:<远程workspace路径>/

scp -r memory/ <用户>@<远程IP>:<远程workspace路径>/memory/
```

**注意权限**：远程文件要 chown 给正确的用户。

### Step 4: 设置定期记忆同步

创建 cron job，定期执行记忆合并。

**合并原则（核心）**：
- **叠加，不覆盖** — 只增不减
- MEMORY.md：对比两边，互相补齐对方没有的内容段
- memory/ 日记（YYYY-MM-DD.md）：按日期补齐缺失文件，同一天的去重合并
- 冲突内容保留两份，标记来源 `<!-- 来源: 实例A -->`

**Cron 配置建议**：每周一次，比如周日 00:00

```
sessionTarget: isolated
schedule: { kind: "cron", expr: "0 0 * * 0", tz: "Asia/Shanghai" }
payload: {
  kind: "agentTurn",
  message: "执行记忆同步：<1> scp 拉取远程的 MEMORY.md 和 memory/ <2> 叠加合并 <3> 推送合并结果回远程 <4> 输出同步报告"
}
```

## 使用方式

搭建完成后，跟本地实例说：
- "让服务器做 XXX" → 本地通过 API 转达给远程
- "把这个文件传到服务器" → scp 直传
- "查一下服务器的 XXX" → API 转达

跟远程实例说也一样，体验无感切换。

## 文件说明

本 skill 包含：

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 本文件，给 OpenClaw 的搭建指南 |
| `scripts/sync-memory.sh` | 记忆同步脚本（可选，也可以让 agent 自行合并） |
| `references/peer-config.json5` | 远程实例连接信息模板 |

## 安全提醒

⚠️ 必须告诉用户：
- API Token = 完全控制权，不要泄露
- 公网 IP 的实例建议用 Tailscale，不要直接暴露
- SSH key 建议加密码保护
- TOOLS.md 里可能有 API key，同步时注意安全
