# OpenClaw Backup Skill

🐈‍⬛ **定期备份 OpenClaw 数据，支持加密、定时、云同步**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

---

## 📋 功能特性

- ✅ **普通备份** - 快速tar.gz压缩
- ✅ **加密备份** - AES-256-CBC加密（推荐）
- ✅ **完整性校验** - SHA256自动验证
- ✅ **定时备份** - cron自动调度
- ✅ **云端同步** - 支持iCloud/Google Drive/Dropbox
- ✅ **自动恢复** - 备份前自动保存当前状态

---

## 🚀 快速开始

### 安装

从 [ClawHub](https://clawhub.com) 安装（推荐）：

```bash
openclaw skills install openclaw-backup
```

或手动下载：

```bash
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/openclaw-backup.git
```

---

### 使用方法

#### 1️⃣ 创建加密备份（推荐）

```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
```

**输入密码后会自动**：
- 停止OpenClaw网关
- 打包 `~/.openclaw` 数据
- AES-256加密
- 生成SHA256校验
- 重启网关

---

#### 2️⃣ 创建普通备份

```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/backup.sh
```

**无密码，快速备份**（适合本地使用）

---

#### 3️⃣ 配置定时备份

```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/setup_cron.sh
```

**选择频率**：
- 每天 23:00
- 每周日 21:00（推荐）
- 每月1日 20:00
- 自定义

---

#### 4️⃣ 查看所有备份

```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/list_backups.sh
```

**输出示例**：
```
🐈‍⬛ OpenClaw 备份列表
位置: /Users/you/Desktop/OpenClaw_Backups

📦 共 2 个备份文件，总计 2.0G

[🔐 加密] openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
  大小: 1.0G | 日期: Mar 13 20:41 | 校验: ✓

[📂 未加密] openclaw_backup_2026-03-13_20-46-27.tar.gz
  大小: 1.0G | 日期: Mar 13 20:47 | 校验: ✓
```

---

## ⚙️ 环境变量

```bash
# 自定义备份目录
export OPENCLAW_BACKUP_DIR="$HOME/Backups/OpenClaw"

# 设置默认密码（不推荐明文）
export OPENCLAW_BACKUP_PASSWORD="your_password"

# 指定备份脚本（用于cron）
export OPENCLAW_BACKUP_SCRIPT="$HOME/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh"
```

---

## 📦 文件结构

```
openclaw-backup/
├── SKILL.md                      # Skill定义（触发词、描述）
├── README.md                     # 本文档
└── scripts/
    ├── backup.sh                 # 普通备份
    ├── backup_encrypted.sh       # 加密备份（推荐）
    ├── setup_cron.sh             # 配置定时备份
    └── list_backups.sh           # 列出所有备份
```

---

## 🔐 加密说明

### 加密算法

- **算法**: AES-256-CBC
- **密钥派生**: PBKDF2 (100,000轮)
- **工具**: OpenSSL

### 手动解密

```bash
openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \
  -in openclaw_backup_2026-03-13_20-40-13.tar.gz.enc \
  -out openclaw_backup.tar.gz \
  -pass pass:YOUR_PASSWORD
```

---

## 🌐 云端同步

### iCloud Drive

```bash
export OPENCLAW_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw_Backups"
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
```

### Google Drive / Dropbox

```bash
export OPENCLAW_BACKUP_DIR="$HOME/Google Drive/OpenClaw_Backups"
# 或
export OPENCLAW_BACKUP_DIR="$HOME/Dropbox/OpenClaw_Backups"
```

---

## 📚 最佳实践

### 3-2-1 备份原则

- **3** 份副本（本地 + 移动硬盘 + 云盘）
- **2** 种介质
- **1** 份异地

### 备份时机

建议在以下操作后手动备份：
- ✅ 修改配置文件
- ✅ 新增 Skill
- ✅ 更新记忆文件（MEMORY.md）
- ✅ 绑定新渠道
- ✅ 修改 API Key
- ✅ 完成重要对话

### 定期验证

每月验证一次备份完整性：

```bash
cd ~/Desktop/OpenClaw_Backups
shasum -c openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256
```

---

## 🐛 故障排查

### 问题1：cron 任务未执行

**检查**：
```bash
crontab -l
tail -f /tmp/openclaw_backup.log
```

**解决**：
```bash
chmod +x ~/.openclaw/skills/openclaw-backup/scripts/*.sh
```

---

### 问题2：加密失败

**症状**：`openssl: command not found`

**解决**：
```bash
brew install openssl
```

---

### 问题3：备份文件过大

**原因**：包含日志文件、临时文件

**解决**：编辑 `backup.sh`，排除不必要的文件

---

## 🤝 配套Skill

- [openclaw-restore](https://github.com/YOUR_USERNAME/openclaw-restore) - 一键恢复OpenClaw数据

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 强大的AI助手框架
- [OpenSSL](https://www.openssl.org) - 加密工具

---

## 📞 支持

- 📖 [完整文档](SKILL.md)
- 💬 [Discord社区](https://discord.com/invite/clawd)
- 🐛 [提交Issue](https://github.com/YOUR_USERNAME/openclaw-backup/issues)

---

**Made with ❤️ by OpenClaw Community**
