---
name: mjolnir-shadow
description: "Mjolnir Shadow (雷神之影) — Automated rotating backup system for OpenClaw workspaces. Creates GPG-encrypted, rotating backups of workspace files, configs, and data to WebDAV storage. Requires bash, curl, Python 3, gpg (gnupg). Optional env var MJOLNIR_SHADOW_PASS for non-interactive GPG decryption. Triggers on backup, data safety, disaster recovery, workspace protection, system backup, 备份, 数据安全, 灾备, 雷神之影."
metadata: {"clawdbot":{"homepage":"https://github.com/king6381/mjolnir-shadow","requires":{"binaries":["bash","curl","python3","gpg"],"env_optional":["MJOLNIR_SHADOW_PASS"]}}}
---

# Mjolnir Shadow (雷神之影) 🌑

Automated rotating backup for OpenClaw workspaces with GPG-encrypted credential storage.

自动轮转备份系统，支持 GPG 加密凭证。

## Requirements / 依赖

- **bash** + **curl** — most Linux/macOS systems
- **Python 3.6+** — for setup wizard
- **GPG (gnupg)** — for credential encryption (recommended)
- **WebDAV server** — Nextcloud, ownCloud, Synology, etc.
- **Env var** (optional): `MJOLNIR_SHADOW_PASS` — GPG passphrase for non-interactive cron runs

## Quick Start / 快速开始

```bash
# 1. Interactive setup (creates encrypted config)
# 1. 交互式配置（创建加密配置）
python3 scripts/setup_backup.py

# 2. Run backup
# 2. 运行备份
bash scripts/backup.sh

# 3. Check status
# 3. 检查状态
cat memory/backup-state.json
```

## How It Works / 工作原理

1. **Decrypt** config via GPG (or read plaintext fallback) / GPG 解密配置
2. **Collect** workspace, configs, strategies, skills into archives / 打包文件
3. **Upload** to WebDAV via `--netrc-file` (credentials never in process listings) / 上传到 WebDAV
4. **Rotate** — keep N newest, delete oldest (FIFO) / 轮转：保留最新 N 个
5. **Clean up** — all temp files removed on exit / 退出时清理临时文件

## Security / 安全

- **GPG AES-256** encrypted credential storage / 凭证加密存储
- **--netrc-file** for all curl calls (backup + restore) — no `-u user:pass` / 所有 curl 调用使用 netrc
- **HTTPS warning** if WebDAV URL is not HTTPS / 非 HTTPS 警告
- **Channel auth excluded** by default (configurable) / 默认排除通道认证 token
- **Temp cleanup** via `trap EXIT` — netrc + archives removed even on failure / 异常退出也清理
- **Secret exclusion** — `.gpg`, `.key`, `.secret`, `.env` always excluded / 始终排除密钥文件

## What Gets Backed Up / 备份内容

| Component / 组件 | Includes / 包含 | Excludes / 排除 |
|-----------|----------|----------|
| **Workspace** | Memory, docs, scripts | .git, node_modules, venv, .env, secrets/*.gpg |
| **Config** | openclaw.json, cron/ | Channel auth (default), *.gpg, *.secret |
| **Strategies** | Strategy files, monitors | venv, __pycache__ |
| **Skills** | Installed skill packages | node_modules, venv, *.gpg |

## Cron / 定时备份

Setup wizard prints the cron command (does not auto-create). Add manually:

配置向导打印 cron 命令（不会自动创建）。手动添加：

```bash
# Every 3 days at 03:00 / 每 3 天凌晨 3 点
openclaw cron add --name "🌑 Mjolnir Shadow" \
  --schedule "0 3 */3 * *" --tz "Asia/Shanghai" \
  --isolated --timeout 300 \
  --message "bash /path/to/scripts/backup.sh"
```

### Non-interactive GPG decryption / 非交互式 GPG 解密

For unattended cron runs, use `gpg-agent` (recommended) or set `MJOLNIR_SHADOW_PASS` via a **secure secret store** — do NOT put plaintext passphrases in cron commands or world-readable files.

非交互运行时，推荐使用 `gpg-agent`，或通过 **安全的密钥存储** 设置 `MJOLNIR_SHADOW_PASS` — **不要** 在 cron 命令或明文文件中写入密码。

```bash
# Recommended: use gpg-agent (pre-cache passphrase)
# 推荐：使用 gpg-agent（预缓存密码）
gpg-connect-agent /bye  # ensure agent is running

# Alternative: read from encrypted credential store
# 备选：从加密凭证存储读取
# export MJOLNIR_SHADOW_PASS="$(your-secret-manager get mjolnir-shadow-pass)"
```

## Restore / 恢复

### 🚀 一键恢复（推荐新手）

```bash
# 方式1: 全自动模式 — 带进度条，一键搞定
bash scripts/restore.sh --auto

# 方式2: 独立恢复引导 — 不依赖 OpenClaw，全新系统也能用
bash scripts/restore-kit.sh
```

**`--auto` 模式**会自动完成：解密配置 → 查找最新备份 → 下载 → 解压 → 恢复全部组件 → 重启 OpenClaw。全程进度条显示，小白友好。

**`restore-kit.sh`** 是完全独立的脚本，不依赖任何已安装技能。适用于：
- 全新系统重装后恢复
- OpenClaw 还没装的时候
- 从另一台机器 SCP 过来直接运行

```bash
# 从另一台机器拷贝过来运行
scp kaixin:/path/to/restore-kit.sh . && bash restore-kit.sh
```

### 手动模式（高级用户）

```bash
bash scripts/restore.sh --list       # List backups / 列出备份
bash scripts/restore.sh --latest     # Restore latest (manual) / 恢复最新（手动确认）
bash scripts/restore.sh --file NAME  # Restore specific / 恢复指定
```

手动模式先解压到临时目录，你可以检查后再决定覆盖哪些组件。

## Configuration Reference / 配置参考

See `references/config-reference.md` for all options. / 详见配置参考文档。
