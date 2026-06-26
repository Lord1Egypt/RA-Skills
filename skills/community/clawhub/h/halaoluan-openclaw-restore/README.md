# OpenClaw Restore Skill

🐈‍⬛ **一键恢复 OpenClaw 数据，支持加密和未加密备份**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

---

## 📋 功能特性

- ✅ **恢复普通备份** - 直接解压tar.gz
- ✅ **恢复加密备份** - 自动解密AES-256-CBC
- ✅ **完整性校验** - SHA256自动验证
- ✅ **智能选择** - 自动选择最新备份
- ✅ **安全恢复** - 恢复前自动备份当前数据
- ✅ **灾难恢复** - 完整的恢复流程指南

---

## 🚀 快速开始

### 安装

从 [ClawHub](https://clawhub.com) 安装（推荐）：

```bash
openclaw skills install openclaw-restore
```

或手动下载：

```bash
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/openclaw-restore.git
```

---

### 使用方法

#### 1️⃣ 恢复最新备份（推荐）

```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_latest.sh
```

**会自动**：
- 查找最新备份（优先加密备份）
- 询问确认
- 验证完整性
- 解密（如果是加密备份）
- 备份当前数据
- 恢复备份数据
- 重启OpenClaw网关

---

#### 2️⃣ 恢复指定备份（普通备份）

```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore.sh \
  ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-46-27.tar.gz
```

**无需密码**，直接恢复

---

#### 3️⃣ 恢复加密备份

```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh \
  ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
```

**输入密码后自动恢复**

---

#### 4️⃣ 列出可恢复的备份

```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/list_restoreable.sh
```

**输出示例**：
```
🐈‍⬛ 可恢复的备份列表
位置: /Users/you/Desktop/OpenClaw_Backups

[1] openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
    类型: 🔐 加密 | 大小: 1.0G | 日期: Mar 13 20:41
    恢复: bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh "..."

[2] openclaw_backup_2026-03-13_20-46-27.tar.gz
    类型: 📂 普通 | 大小: 1.0G | 日期: Mar 13 20:47
    恢复: bash ~/.openclaw/skills/openclaw-restore/scripts/restore.sh "..."
```

---

## 🔄 恢复流程

### 完整流程（自动执行）

1. **验证备份** - 检查SHA256校验和
2. **解密**（如需要） - AES-256-CBC解密
3. **停止网关** - 停止OpenClaw服务
4. **备份当前数据** - 保存到 `~/.openclaw.backup.YYYYMMDD_HHMMSS`
5. **恢复数据** - 解压并覆盖 `~/.openclaw`
6. **修复检查** - 运行 `openclaw doctor`
7. **重启网关** - 启动OpenClaw服务

---

## ✅ 恢复后检查清单

### 必检项目

```bash
# 1. 网关状态
openclaw status

# 2. 配置验证
openclaw doctor

# 3. 记忆文件
cat ~/.openclaw/workspace/MEMORY.md

# 4. API配置
cat ~/.openclaw/config.yaml | grep -A5 "model:"
```

### 可能需要重新配置

- ❓ Telegram Bot - 检查是否在线
- ❓ WeChat - 可能需要重新扫码
- ❓ 渠道登录状态

---

## 🆘 灾难恢复指南

### 场景：macOS 完全重装

#### 第1步：安装 Node.js + OpenClaw

```bash
# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node

# 安装 OpenClaw
npm install -g openclaw
```

---

#### 第2步：恢复备份

```bash
# 从云盘/移动硬盘拷贝备份文件
cp /Volumes/External/openclaw_backup_*.tar.gz.enc ~/Desktop/

# 下载恢复Skill
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/openclaw-restore.git

# 恢复
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh \
  ~/Desktop/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
```

---

#### 第3步：验证

```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

---

## 📦 文件结构

```
openclaw-restore/
├── SKILL.md                      # Skill定义
├── README.md                     # 本文档
└── scripts/
    ├── restore.sh                # 恢复普通备份
    ├── restore_encrypted.sh      # 恢复加密备份
    └── restore_latest.sh         # 恢复最新备份
```

---

## ⚙️ 环境变量

```bash
# 备份目录位置
export OPENCLAW_BACKUP_DIR="$HOME/Desktop/OpenClaw_Backups"

# 设置默认密码（不推荐明文）
export OPENCLAW_BACKUP_PASSWORD="your_password"
```

---

## 🐛 故障排查

### 问题1：解密失败

**症状**：`bad decrypt`

**原因**：密码错误或文件损坏

**解决**：
1. 确认密码正确
2. 验证备份完整性：`shasum -c backup.tar.gz.enc.sha256`
3. 尝试恢复更早的备份

---

### 问题2：恢复后网关无法启动

**症状**：`openclaw gateway start` 失败

**解决**：
```bash
# 检查配置
openclaw doctor

# 查看日志
tail -f ~/.openclaw/logs/gateway.log

# 重置配置（谨慎）
mv ~/.openclaw/config.yaml ~/.openclaw/config.yaml.broken
openclaw gateway start
```

---

### 问题3：权限问题

**症状**：`Permission denied`

**解决**：
```bash
chmod -R 755 ~/.openclaw
chmod 600 ~/.openclaw/config.yaml
```

---

## 🔐 安全特性

### 自动备份当前数据

恢复前会自动备份当前数据到：
```
~/.openclaw.backup.YYYYMMDD_HHMMSS
```

确认恢复成功后可删除：
```bash
rm -rf ~/.openclaw.backup.20260313_204600
```

### 完整性验证

恢复前会自动验证SHA256校验和，确保备份未被篡改

---

## 🤝 配套Skill

- [openclaw-backup](https://github.com/YOUR_USERNAME/openclaw-backup) - 定期备份OpenClaw数据

---

## 📚 最佳实践

### 1. 恢复前验证备份

```bash
shasum -c backup.tar.gz.sha256
```

### 2. 小范围测试

先恢复到临时位置测试：
```bash
tar -xzf backup.tar.gz -C /tmp/test_restore
```

### 3. 保留多个备份

建议保留至少3个不同时间点的备份

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
- 🐛 [提交Issue](https://github.com/YOUR_USERNAME/openclaw-restore/issues)

---

**Made with ❤️ by OpenClaw Community**
