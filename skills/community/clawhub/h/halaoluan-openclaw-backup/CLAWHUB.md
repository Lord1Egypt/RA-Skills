# ClawHub 提交信息

## 基本信息

**Skill名称**: openclaw-backup  
**版本**: 1.0.0  
**作者**: Weifeng Zhao (@halaoluan)  
**许可**: MIT  
**分类**: Utilities, Backup, Security  

---

## 简短描述

🐈‍⬛ 定期备份 OpenClaw 数据，支持AES-256加密、定时备份、云端同步。保护你的配置、记忆、Skills不丢失。

---

## 详细描述

OpenClaw Backup 是一个专业的备份解决方案，帮助你安全地保存 OpenClaw 的所有数据：

### 核心功能
- ✅ **加密备份** - AES-256-CBC加密（PBKDF2 100,000轮）
- ✅ **完整性校验** - SHA256自动验证
- ✅ **定时备份** - cron自动调度（每天/每周/每月）
- ✅ **云端同步** - 支持iCloud/Google Drive/Dropbox
- ✅ **多版本管理** - 保留多个备份版本
- ✅ **一键操作** - 简单易用的命令行界面

### 为什么需要备份？
OpenClaw 包含重要数据：
- 🔑 API Key和渠道配置
- 🧠 记忆文件（MEMORY.md、对话历史）
- 🛠️ 自定义Skills和脚本
- 📱 渠道登录状态（Telegram、WeChat等）

一旦丢失，需要重新配置所有内容。定期备份可以：
- 防止意外删除
- 系统崩溃快速恢复
- 换设备无缝迁移
- 测试新功能前保存状态

### 安全性
- 🔐 AES-256军事级加密
- 🔒 PBKDF2密钥派生（抗暴力破解）
- ✅ SHA256完整性验证
- 🛡️ 符合NIST安全标准

### 易用性
- 📋 一条命令完成备份
- ⏰ 自动定时备份
- ☁️ 自动云端同步
- 📊 清晰的备份列表

### 配套工具
配合 [openclaw-restore](https://github.com/halaoluan/openclaw-restore) 使用，实现完整的备份+恢复解决方案。

---

## 安装

```bash
openclaw skills install openclaw-backup
```

或手动安装：

```bash
cd ~/.openclaw/skills
git clone https://github.com/halaoluan/openclaw-backup.git
```

---

## 快速开始

### 创建加密备份
```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
```

### 查看备份列表
```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/list_backups.sh
```

### 配置定时备份
```bash
bash ~/.openclaw/skills/openclaw-backup/scripts/setup_cron.sh
```

---

## 截图/演示

（建议添加实际截图或GIF）

---

## 文档

- 📖 [README.md](https://github.com/halaoluan/openclaw-backup/blob/main/README.md) - 完整使用指南
- 🎬 [DEMO.md](https://github.com/halaoluan/openclaw-backup/blob/main/DEMO.md) - 演示和示例
- 🚀 [ADVANCED.md](https://github.com/halaoluan/openclaw-backup/blob/main/ADVANCED.md) - 高级配置
- ❓ [FAQ.md](https://github.com/halaoluan/openclaw-backup/blob/main/FAQ.md) - 常见问题

---

## 依赖

- macOS 10.15+ 或 Linux
- Bash 4.0+
- OpenSSL（加密功能）
- tar, gzip（压缩）

---

## 标签

`backup` `encryption` `security` `automation` `cron` `aes-256` `cloud-sync` `disaster-recovery`

---

## GitHub仓库

https://github.com/halaoluan/openclaw-backup

---

## 支持

- 🐛 [提交Issue](https://github.com/halaoluan/openclaw-backup/issues)
- 💬 [Discord讨论](https://discord.com/invite/clawd)
- 📧 Email: halaoluan18@gmail.com

---

## 更新日志

### v1.0.0 (2026-03-13)
- ✨ 初始发布
- ✅ 支持AES-256加密备份
- ✅ 支持定时备份（cron）
- ✅ 完整的文档（README、FAQ、高级指南）
- ✅ 云端同步支持
