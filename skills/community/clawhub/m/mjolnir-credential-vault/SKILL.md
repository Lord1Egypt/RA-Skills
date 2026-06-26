---
name: credential-vault
version: 1.3.1
description: "GPG AES-256 encrypted credential management. Requires: GPG (gnupg) installed, Python 3.8+, CRED_MASTER_PASS env var for non-interactive use. Use when the user needs to securely store, retrieve, or manage passwords, API tokens, and secrets. Supports init/add/get/list/remove operations. Triggers: password management, secret storage, credential encryption, token vault, secure credentials, 凭证管理, 密码加密, 安全存储."
metadata:
  clawdbot:
    requires:
      bins:
        - gpg
        - python3
      env:
        - CRED_MASTER_PASS
---

# 🛡️ Credential Vault / 凭证保险箱

GPG AES-256 encrypted credential manager — one file, all secrets.  
GPG AES-256 对称加密凭证管理器 — 一个文件，管理所有密钥。

> ⚡🔨 Part of the Mjölnir / 雷神 toolchain  
> 🛡️ Brand: 雷神之盾 (Shield of Thor)

---

## Dependencies / 依赖

- **Python 3.8+**
- **GPG (gnupg)** — pre-installed on most Linux/macOS; Windows needs [Gpg4win](https://gpg4win.org)
- Check / 检查: `gpg --version` (the `init` command verifies this automatically / `init` 命令会自动检查)

## Required Environment Variables / 环境变量

| Variable / 变量 | Purpose / 用途 | Required? / 是否必需 |
|----------|---------|-----------|
| `CRED_MASTER_PASS` | Master password for encrypt/decrypt / 加解密主密码 | Required for non-interactive use; prompts if unset / 非交互使用时必需；未设置则交互输入 |

---

## Quick Start / 快速开始

```bash
# Initialize (first time) / 首次初始化 — checks GPG availability / 检查 GPG 可用性
python3 SKILL_DIR/scripts/cred_manager.py init

# Add credentials (interactive) / 交互式添加凭证
python3 SKILL_DIR/scripts/cred_manager.py add myservice

# Non-interactive use / 非交互使用
export CRED_MASTER_PASS="your_password"
```

Replace `SKILL_DIR` with the actual skill directory path.  
将 `SKILL_DIR` 替换为实际的技能目录路径。

---

## Security Model / 安全模型

### How it works / 工作原理

1. All credentials stored as AES-256 encrypted `.gpg` file (permissions 600)  
   所有凭证存储为 AES-256 加密的 `.gpg` 文件（权限 600）
2. Master password passed to GPG via `--passphrase-fd` (stdin pipe) — **never** in command-line arguments  
   主密码通过 `--passphrase-fd`（stdin 管道）传递给 GPG — **绝不**出现在命令行参数中
3. Shell helper also uses `--passphrase-fd 0` (echo pipe) — **not** `--passphrase`  
   Shell 辅助脚本同样使用 `--passphrase-fd 0`（echo 管道）— **不用** `--passphrase`

### Temporary plaintext on disk / 临时明文落盘

During save/encrypt operations, plaintext JSON briefly exists as a temporary file:  
在保存/加密操作期间，明文 JSON 会短暂存在于临时文件中：

- Created with `mkstemp` + `fchmod 600` (owner-only read/write) / 使用 `mkstemp` + `fchmod 600` 创建（仅所有者可读写）
- Exists for milliseconds (only during GPG subprocess execution) / 仅存在毫秒级（GPG 子进程执行期间）
- Securely deleted: zero-overwrite → fsync → unlink / 安全删除：零覆写 → fsync → unlink
- **Risk / 风险**: on some systems, temp file contents may be recoverable from disk. For higher security, use a tmpfs/ramfs mount or a dedicated secrets manager.  
  在某些系统上，临时文件内容可能可从磁盘恢复。如需更高安全性，请使用 tmpfs/ramfs 挂载或专用密钥管理器。

### Master password storage / 主密码存储

The `CRED_MASTER_PASS` environment variable is readable by same-user processes via `/proc/*/environ` on Linux.  
`CRED_MASTER_PASS` 环境变量在 Linux 上可被同用户进程通过 `/proc/*/environ` 读取。

**Recommended approaches (most → least secure) / 推荐方式（安全性从高到低）：**

1. **gpg-agent / pinentry** — enter password interactively each time (most secure) / 每次交互输入密码（最安全）
2. **Runtime injection / 运行时注入** — set via a secrets manager or session-scoped `read -s` prompt / 通过密钥管理器或会话级 `read -s` 提示设置
3. **Environment variable / 环境变量** — `export CRED_MASTER_PASS="..."` in current shell (convenient but less secure) / 在当前 shell 中设置（方便但安全性较低）

**Avoid / 避免:** persisting the master password in plaintext files (e.g., `~/.bashrc`). If you must, ensure `chmod 600` and understand the trade-off.  
不要将主密码明文写入文件（如 `~/.bashrc`）。如必须，请确保 `chmod 600` 并了解风险。

---

## Core Operations / 核心操作

### Initialize / 初始化

```bash
python3 scripts/cred_manager.py init
```

Verifies GPG is installed, creates encrypted `credentials.json.gpg` (permissions 600). Warns if password < 8 chars.  
验证 GPG 已安装，创建加密的 `credentials.json.gpg`（权限 600）。密码少于 8 位会警告。

### Add / Update Credentials / 添加/更新凭证

```bash
python3 scripts/cred_manager.py add <service_name>
# Interactive: enter key=value pairs, empty line to finish
# 交互式：输入 key=value 键值对，空行结束
```

Or programmatically / 或通过代码调用：

```python
from cred_manager import add_credential
add_credential('github', {'user': 'octocat', 'token': 'ghp_xxx'})
```

### Retrieve Credentials / 获取凭证

**Python:**
```python
from cred_manager import get_credential, get_service

token = get_credential('github', 'token')    # single field / 单个字段
config = get_service('github')               # full dict / 完整字典
```

**Shell / Bash:**
```bash
export CRED_MASTER_PASS="your_password"
source scripts/cred_helper.sh
TOKEN=$(cred_get github token)
```

**CLI / 命令行:**
```bash
python3 scripts/cred_manager.py get github token
python3 scripts/cred_manager.py list
```

### Remove / 删除

```bash
python3 scripts/cred_manager.py remove <service_name>
```

---

## Integration Pattern / 集成模式

When a script has hardcoded passwords, refactor to:  
当脚本中有硬编码密码时，重构为：

```python
import sys, os
sys.path.insert(0, os.path.expanduser('path/to/credential-vault/scripts'))
from cred_manager import get_credential

password = get_credential('myservice', 'pass')
```

---

## Known Limitations / 已知限制

1. **Temporary plaintext on disk / 临时明文落盘** — briefly exists during encrypt operations (mitigated but not zero-risk) / 加密操作时短暂存在（已缓解但非零风险）
2. **Environment variable visibility / 环境变量可见性** — `CRED_MASTER_PASS` readable by same-user processes on Linux / 在 Linux 上可被同用户进程读取
3. **No key rotation / 无密钥轮换** — manual re-encrypt required to change master password / 更换主密码需手动重新加密
4. **Single-user design / 单用户设计** — not for enterprise multi-tenant use / 不适用于企业多租户场景
5. **No tamper detection / 无篡改检测** — `.gpg` file integrity not independently verified / `.gpg` 文件完整性未独立验证

For higher security requirements, consider: OS keyring, `pass`, HashiCorp Vault, or cloud KMS.  
如需更高安全性，请考虑：OS 密钥环、`pass`、HashiCorp Vault 或云 KMS。

---

## Changelog / 更新日志

- **v1.3.1** — Fix registry metadata: declare `gpg`, `python3` bins and `CRED_MASTER_PASS` env var / 修复注册表元数据：声明依赖二进制和环境变量
- **v1.3.0** — Bilingual documentation (EN/CN) / 中英双语文档；bilingual CLI output / 双语 CLI 输出
- **v1.2.0** — Security hardening: `--passphrase-fd` for both Python & Shell; honest temp-file disclosure; 3-tier password advice / 安全加固
- **v1.1.0** — Python `--passphrase-fd` stdin pipe / Python 端 stdin 管道传密码
- **v1.0.0** — Initial release / 首次发布
