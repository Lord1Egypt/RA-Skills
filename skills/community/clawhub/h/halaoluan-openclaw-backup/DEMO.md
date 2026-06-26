# OpenClaw Backup - 演示

## 🎬 快速演示

### 创建加密备份

```bash
$ bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
```

**输出**：
```
🐈‍⬛ OpenClaw 加密备份开始...
请输入备份密码（至少8位）:
请再次输入密码:

✓ 发现: /Users/you/.openclaw
⏸  停止 OpenClaw 网关...
📦 打包中...
🔐 加密中...
▶️  重启 OpenClaw 网关...

✅ 加密备份完成！
📁 位置: ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
🔐 校验: ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256

⚠️  请妥善保管密码！丢失密码将无法恢复数据。
```

---

### 查看备份列表

```bash
$ bash ~/.openclaw/skills/openclaw-backup/scripts/list_backups.sh
```

**输出**：
```
🐈‍⬛ OpenClaw 备份列表
位置: /Users/you/Desktop/OpenClaw_Backups

📦 共 2 个备份文件，总计 2.0G

[🔐 加密] openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
  大小: 1.0G | 日期: Mar 13 20:41 | 校验: ✓

[📂 未加密] openclaw_backup_2026-03-13_20-46-27.tar.gz
  大小: 1.0G | 日期: Mar 13 20:47 | 校验: ✓

验证备份完整性：
  shasum -c openclaw_backup_XXXX.tar.gz.sha256
```

---

### 配置定时备份

```bash
$ bash ~/.openclaw/skills/openclaw-backup/scripts/setup_cron.sh
```

**输出**：
```
🐈‍⬛ 配置 OpenClaw 定时备份

选择备份频率：
1. 每天 23:00
2. 每周日 21:00
3. 每月1日 20:00
4. 自定义

请选择 [1-4]: 2

✅ 定时备份已配置
📅 频率: 每周日 21:00
📜 脚本: ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh

查看所有定时任务: crontab -l
查看备份日志: tail -f /tmp/openclaw_backup.log
```

---

## 📸 截图

### 备份完成后的文件

```
OpenClaw_Backups/
├── openclaw_backup_2026-03-13_20-40-13.tar.gz.enc      (1.0 GB) 🔐
├── openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256  (87 B) ✓
├── openclaw_backup_2026-03-13_20-46-27.tar.gz          (1.0 GB) 📂
└── openclaw_backup_2026-03-13_20-46-27.tar.gz.sha256      (83 B) ✓
```

---

## 🎯 核心特性演示

### 1. AES-256 加密

```bash
# 加密算法信息
Algorithm: AES-256-CBC
Key Derivation: PBKDF2 (100,000 iterations)
Salt: Random (per backup)
```

### 2. SHA256 校验

```bash
$ shasum -c openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256
/Users/you/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc: OK
```

### 3. 自动化定时备份

```bash
$ crontab -l
0 21 * * 0 /Users/you/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh >> /tmp/openclaw_backup.log 2>&1
```

---

## 📊 性能数据

| 操作 | 耗时 | 文件大小 |
|------|------|---------|
| 打包 | ~30s | 1.0 GB → 1.0 GB (已压缩) |
| 加密 | ~15s | 1.0 GB → 1.0 GB |
| 校验 | ~5s | SHA256 |
| 总计 | ~50s | - |

---

## 🔗 相关链接

- [完整文档](https://github.com/halaoluan/openclaw-backup)
- [恢复工具](https://github.com/halaoluan/openclaw-restore)
- [ClawHub](https://clawhub.com)
