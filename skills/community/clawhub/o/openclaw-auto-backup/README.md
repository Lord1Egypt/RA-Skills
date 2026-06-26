# Auto Backup for OpenClaw - 自动备份技能

自动备份 OpenClaw 配置文件，保护配置安全。

[English Version](README_EN.md)

---

## 🎯 推荐安装场景

✅ **你应该安装这个技能，如果：**
- [ ] 你是 OpenClaw 新手，想保护配置
- [ ] 你需要定时自动备份
- [ ] 你担心配置丢失
- [ ] 你需要版本管理
- [ ] 你在团队中协作

❌ **不需要安装，如果：**
- [ ] 你手动备份配置
- [ ] 你使用外部备份工具
- [ ] 你是临时测试使用

---

## ⭐ 觉得好用？

如果喜欢这个技能，请：
1. 在 ClawHub 给个 **⭐⭐⭐⭐⭐ 5 星好评**
2. 分享给其他 OpenClaw 用户
3. 提交 Issue 或 PR 改进

**你的评分对我们很重要！** 帮助更多人发现这个技能。

---

## 🔗 相关技能推荐

安装了这个技能的用户也安装了：

| 技能 | 作用 | 推荐度 |
|------|------|--------|
| [Model Switch](../model-switch) | 切换 AI 模型 | ⭐⭐⭐⭐⭐ |
| [Memory Enhancer](../memory-enhancer) | 增强记忆 | ⭐⭐⭐⭐⭐ |
| [Search Pro](../search-pro) | 联网搜索 | ⭐⭐⭐⭐ |

**推荐组合安装：**
```bash
npx clawhub install openclaw-auto-backup
npx clawhub install openclaw-model-switch
npx clawhub install openclaw-memory-enhancer
```

---

## ✨ 功能特性

- 📦 **手动备份** - 随时备份配置
- ⏰ **定时备份** - 每天凌晨 2 点自动备份
- 📚 **版本管理** - 查看所有备份版本
- 🔄 **一键恢复** - 恢复到任意版本
- 🧹 **自动清理** - 保留最近 N 个备份

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/auto-backup
chmod +x auto-backup/scripts/*.py
```

---

## 📖 使用

### 备份配置

```bash
# 手动备份
python3 auto-backup/scripts/backup.py

# 带备注备份
python3 auto-backup/scripts/backup.py --note "配置更新后"
```

### 查看备份

```bash
python3 auto-backup/scripts/list.py
```

### 恢复配置

```bash
# 恢复到指定版本
python3 auto-backup/scripts/restore.py --version backup-20260310-195545

# 恢复到上一个版本
python3 auto-backup/scripts/restore.py --offset -1
```

### 清理备份

```bash
# 保留最近 10 个
python3 auto-backup/scripts/cleanup.py --keep 10

# 删除超过 30 天的
python3 auto-backup/scripts/cleanup.py --older-than 30d
```

---

## ⏰ 定时任务

已配置每天凌晨 2 点自动备份。

查看定时任务：
```bash
openclaw cron list
```

---

## 📋 配置

备份配置：
`~/.openclaw/workspace/skills/auto-backup/config/backup-config.json`

备份位置：
`~/.openclaw/backups/`

---

## 🛠️ 脚本说明

| 脚本 | 功能 |
|------|------|
| `backup.py` | 备份配置 |
| `list.py` | 查看备份列表 |
| `restore.py` | 恢复配置 |
| `cleanup.py` | 清理旧备份 |

---

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.0

---

## 🔒 安全说明

- **本地执行：** 所有脚本在本地运行，不联网
- **权限范围：** 仅需读取 ~/.openclaw/ 目录
- **无外部依赖：** 不克隆外部仓库，所有代码已包含
- **数据安全：** 不上传任何数据到外部服务器

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
