# ClawHub 提交信息

## 基本信息

**Skill名称**: openclaw-restore  
**版本**: 1.0.0  
**作者**: Weifeng Zhao (@halaoluan)  
**许可**: MIT  
**分类**: Utilities, Recovery, Disaster Recovery  

---

## 简短描述

🐈‍⬛ 一键恢复 OpenClaw 数据，支持加密和未加密备份。系统崩溃？数据丢失？快速恢复到正常状态。

---

## 详细描述

OpenClaw Restore 是一个专业的数据恢复工具，配合 openclaw-backup 使用，提供完整的灾难恢复解决方案。

### 核心功能
- ✅ **智能恢复** - 自动选择最新备份
- ✅ **加密支持** - 解密AES-256-CBC备份
- ✅ **完整性验证** - SHA256自动校验
- ✅ **安全恢复** - 恢复前自动备份当前数据
- ✅ **快速恢复** - 一条命令完成全部流程
- ✅ **灾难恢复** - 完整的macOS重装恢复指南

### 适用场景
- 🔴 **系统崩溃** - macOS重装、硬盘损坏
- 🟠 **误操作** - 删除了重要配置/数据
- 🟡 **设备迁移** - 换新电脑无缝迁移
- 🟢 **版本回退** - OpenClaw升级失败
- 🔵 **测试环境** - 快速搭建开发/测试环境

### 安全特性
- 🔐 自动解密AES-256备份
- 🔒 恢复前备份当前数据（防止误操作）
- ✅ SHA256完整性验证
- 🛡️ 手动确认机制（防止误恢复）

### 恢复流程
1. 验证备份完整性（SHA256）
2. 解密（如需要）
3. 停止OpenClaw网关
4. 备份当前数据到 `~/.openclaw.backup.YYYYMMDD_HHMMSS`
5. 恢复备份数据
6. 运行修复检查（`openclaw doctor`）
7. 重启网关

### 灾难恢复
提供完整的macOS重装后恢复流程：
1. 安装基础环境（Node.js + OpenClaw）
2. 从云盘/移动硬盘恢复备份
3. 验证和启动

### 易用性
- 📋 一条命令恢复最新备份
- 🔍 智能选择加密/未加密备份
- ✅ 自动验证和修复
- 📊 清晰的恢复过程提示

### 配套工具
配合 [openclaw-backup](https://github.com/halaoluan/openclaw-backup) 使用，实现完整的备份+恢复解决方案。

---

## 安装

```bash
openclaw skills install openclaw-restore
```

或手动安装：

```bash
cd ~/.openclaw/skills
git clone https://github.com/halaoluan/openclaw-restore.git
```

---

## 快速开始

### 恢复最新备份
```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_latest.sh
```

### 恢复指定备份（普通）
```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore.sh /path/to/backup.tar.gz
```

### 恢复加密备份
```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh /path/to/backup.tar.gz.enc
```

---

## 截图/演示

（建议添加实际截图或GIF）

---

## 文档

- 📖 [README.md](https://github.com/halaoluan/openclaw-restore/blob/main/README.md) - 完整使用指南
- ❓ [FAQ.md](https://github.com/halaoluan/openclaw-restore/blob/main/FAQ.md) - 23个常见问题解答
- 🆘 灾难恢复流程（在README中）

---

## 依赖

- macOS 10.15+ 或 Linux
- Bash 4.0+
- OpenSSL（解密功能）
- tar, gzip（解压）
- openclaw-backup（创建备份）

---

## 标签

`restore` `recovery` `disaster-recovery` `backup` `encryption` `migration` `data-protection`

---

## GitHub仓库

https://github.com/halaoluan/openclaw-restore

---

## 支持

- 🐛 [提交Issue](https://github.com/halaoluan/openclaw-restore/issues)
- 💬 [Discord讨论](https://discord.com/invite/clawd)
- 📧 Email: halaoluan18@gmail.com

---

## 更新日志

### v1.0.0 (2026-03-13)
- ✨ 初始发布
- ✅ 支持恢复加密备份
- ✅ 智能选择最新备份
- ✅ 完整的灾难恢复指南
- ✅ 23个FAQ解答
