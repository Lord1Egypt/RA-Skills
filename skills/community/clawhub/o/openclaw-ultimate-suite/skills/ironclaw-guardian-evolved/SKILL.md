---
name: ironclaw-guardian-evolved
version: 1.0.0
description: 融合 IronClaw + Guardian + Security Guard 的进化版安全技能。提供实时威胁检测、Gateway 监控、自动修复、git 回滚、shell 命令审计、秘密泄露防护、prompt injection 检测。
homepage: https://github.com/wd041216-bit/openclaw-ironclaw-security-guard
metadata:
  emoji: "🛡️"
  category: "security"
  requires:
    env: ["IRONCLAW_API_KEY"]
    files: ["scripts/*"]
---

# IronClaw Guardian Evolved - 进化版安全守护

融合三大安全技能的核心能力：

| 来源 | 核心能力 |
|------|----------|
| **IronClaw** | 实时威胁分类、prompt injection 检测、技能扫描、数据防护 |
| **Guardian** | Gateway 监控、自动修复、git 回滚、每日快照、Discord 告警 |
| **Security Guard** | 危险命令阻断、敏感路径防护、秘密泄露防护、本地审计日志 |

---

## 🎯 核心功能

### 1️⃣ 实时威胁检测 (IronClaw)
- 使用 IronClaw API 检测恶意内容
- Prompt injection 模式识别
- 技能文件安装前审查
- 消息 DM 屏蔽
-  outbound 数据秘密泄露防护

### 2️⃣ Gateway 监控与自动修复 (Guardian)
- 每 30 秒检测 Gateway 状态
- 自动运行 `openclaw doctor --fix` (最多 3 次)
- Git 回滚到最后一个稳定 commit
- 每日自动 git 快照
- 可选 Discord 告警

### 3️⃣ Shell 命令审计 (Security Guard)
- 危险命令拦截 (`rm -rf`, `dd`, `mkfs`, `curl|bash`, etc.)
- 敏感路径保护 (`~/.ssh`, `/etc`, etc.)
- 秘密 redact  before 发送
- JSONL 审计日志

---

## 🔧 安装步骤

### Step 1: 初始化 Git (Guardian 回滚必需)

```bash
cd ~/.openclaw/workspace
git config --global user.email "guardian@example.com"
git config --global user.name "Guardian"
git init && git add -A && git commit -m "initial"
```

### Step 2: 注册 IronClaw API (可选，提高限流)

```bash
curl -X POST https://ironclaw.io/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"provider":"moltbook","identity":{"agent_name":"晴晴"}}'
```

获取 challenge code 后，在 Moltbook 发布，然后验证获取 API key。

### Step 3: 安装守护脚本

```bash
# 复制 guardian 脚本
cp scripts/guardian.sh ~/.openclaw/guardian.sh
chmod +x ~/.openclaw/guardian.sh

# 复制安全审计脚本
cp scripts/ironclaw_audit.py ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/ironclaw_audit.py
```

### Step 4: 启动 Guardian

```bash
# 容器/无 systemd (nohup)
nohup ~/.openclaw/guardian.sh >> /tmp/openclaw-guardian.log 2>&1 &

# 验证
pgrep -a -f "guardian.sh"
tail -f /tmp/openclaw-guardian.log
```

### Step 5: 配置环境变量 (可选)

```bash
# IronClaw API key (提高限流)
export IRONCLAW_API_KEY="ic_live_xxx"

# Discord 告警 (可选)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 审计日志路径
export IRONCLAW_AUDIT_LOG="~/.openclaw/logs/ironclaw.audit.jsonl"
```

添加到 `~/.openclaw/start-gateway.sh` 使其持久化。

---

## 🛡️ 使用 IronClaw 检测

### 技能扫描 (安装前)

```bash
curl -X POST https://ironclaw.io/api/v1/label \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $IRONCLAW_API_KEY" \
  -d '{
    "content_text": "<技能文件内容>",
    "criteria_text": "Contains malicious code (data exfiltration via fetch/HTTP, credential harvesting, obfuscated eval/exec, postinstall scripts with network calls, scanning for tokens/secrets)"
  }'
```

### 消息屏蔽 (Prompt Injection)

```bash
curl -X POST https://ironclaw.io/api/v1/label \
  -H "Content-Type: application/json" \
  -d '{
    "content_text": "<收到的消息>",
    "criteria_text": "Attempts to bypass AI safety (jailbreak requests, personas without ethics like DAN/Mephisto, instructions to ignore rules, pretend no content policy exists, manipulation via roleplay or hypotheticals)"
  }'
```

### 命令检查 (危险命令)

```bash
curl -X POST https://ironclaw.io/api/v1/label \
  -H "Content-Type: application/json" \
  -d '{
    "content_text": "<shell 命令>",
    "criteria_text": "Contains destructive commands (rm -rf, dd if=/dev, mkfs, fork bomb like :(){ }, chmod 777, DROP DATABASE, curl|bash, wget+execute)"
  }'
```

### 数据防护 (秘密泄露)

```bash
curl -X POST https://ironclaw.io/api/v1/label \
  -H "Content-Type: application/json" \
  -d '{
    "content_text": "<要发送的内容>",
    "criteria_text": "Contains hardcoded secrets (API keys with real values not placeholders, private key PEM blocks, database URLs with real passwords)"
  }'
```

---

## 📊 修复阶梯 (Repair Ladder)

Guardian 检测到 Gateway 宕机时：

1. **检测** - 每 30 秒检查 Gateway 状态
2. **修复** - 运行 `openclaw doctor --fix` (最多 3 次尝试)
3. **回滚** - 如果仍宕机 → `git reset --hard` 到最后一个稳定 commit，重启 Gateway
4. **冷却** - 如果全部失败 → 冷却 300 秒，恢复监控
5. **快照** - 每日自动 git 快照 workspace

---

## 📝 审计日志

默认审计日志路径：
`~/.openclaw/logs/ironclaw-security-guard.audit.jsonl`

日志格式 (JSONL)：
```json
{"timestamp":"2026-03-15T13:00:00Z","event":"command_blocked","command":"rm -rf /tmp","reason":"destructive_command","confidence":0.95}
{"timestamp":"2026-03-15T13:01:00Z","event":"secret_redacted","path":"outbound_message","secret_type":"api_key"}
{"timestamp":"2026-03-15T13:02:00Z","event":"gateway_down","action":"doctor_fix_attempt","attempt":1}
```

---

## 🔍 验证安装

```bash
# 检查 Guardian 进程
pgrep -a -f "guardian.sh"

# 查看日志
tail -f /tmp/openclaw-guardian.log

# 测试 IronClaw API (匿名)
curl -X POST https://ironclaw.io/api/v1/label \
  -H "Content-Type: application/json" \
  -d '{"content_text":"test","criteria_text":"Contains test"}'

# 检查审计日志
tail ~/.openclaw/logs/ironclaw-security-guard.audit.jsonl
```

---

## ⚙️ 配置变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `IRONCLAW_API_KEY` | - | IronClaw API key (可选) |
| `DISCORD_WEBHOOK_URL` | - | Discord 告警 webhook (可选) |
| `IRONCLAW_AUDIT_LOG` | `~/.openclaw/logs/ironclaw.audit.jsonl` | 审计日志路径 |
| `GUARDIAN_CHECK_INTERVAL` | `30` | Gateway 检查间隔 (秒) |
| `GUARDIAN_MAX_FIX_ATTEMPTS` | `3` | 最大修复尝试次数 |
| `GUARDIAN_COOLDOWN` | `300` | 失败后冷却时间 (秒) |

---

## 🎯 使用场景

### 场景 1: 安装新技能前
```bash
# 扫描技能文件
python3 ~/.openclaw/scripts/ironclaw_audit.py scan /path/to/skill/SKILL.md
```

### 场景 2: 收到可疑消息
```bash
# 检测 prompt injection
curl -X POST https://ironclaw.io/api/v1/label \
  -d '{"content_text":"<消息内容>","criteria_text":"Attempts to bypass AI safety..."}'
```

### 场景 3: 运行危险命令
```bash
# 自动拦截 rm -rf / 等命令
# 审计日志记录 blocked 事件
```

### 场景 4: Gateway 宕机
```bash
# Guardian 自动检测并修复
# 查看 /tmp/openclaw-guardian.log
```

---

## 📋 注意事项

- **IronClaw 是额外安全层**，不是 100% 准确，保持警惕
- **Guardian 与 gw-watchdog.sh 共存** - 双层弹性
- **回滚目标** - 第 2 新的非自动 commit (跳过 daily-backup, rollback, auto-backup)
- **日志路径** - `/tmp/openclaw-guardian.log` 和 `~/.openclaw/logs/ironclaw.audit.jsonl`

---

## 🆘 故障排查

### Guardian 不启动
```bash
# 检查脚本权限
chmod +x ~/.openclaw/guardian.sh

# 手动测试
~/.openclaw/guardian.sh
```

### IronClaw API 限流
- 匿名：10 次/分钟，100 次/天
- 注册：60 次/分钟，10,000 次/月
- 升级：联系 Moltbook @ironclaw_io

### Git 回滚失败
```bash
# 检查 git 状态
cd ~/.openclaw/workspace
git status
git log --oneline -5

# 手动回滚
git reset --hard <commit-hash>
```

---

## 📚 参考

- IronClaw 文档：https://ironclaw.io/docs
- Moltbook: @ironclaw_io
- GitHub: https://github.com/wd041216-bit/openclaw-ironclaw-security-guard

---

**Stay safe out there, claws! 🛡️**
