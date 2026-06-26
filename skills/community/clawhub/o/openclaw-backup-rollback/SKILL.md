# OpenClaw 备份回滚系统

自动备份 + 回滚系统，保护OpenClaw配置安全。

## 功能

- **自动备份**：每15分钟自动备份整个 `.openclaw` 目录
- **手动备份**：执行 `/backup` 立即备份
- **版本回滚**：执行 `/rollback` 查看所有版本并选择还原
- **预览差异**：还原前可查看备份与当前配置的差异
- **暂不还原**：可取消操作
- **压缩存储**：仅11MB/个，保留最近96个（约24小时）

## 使用方式

| 命令 | 说明 |
|------|------|
| `/backup` | 立即执行一次备份 |
| `/backup list` | 列出所有可用备份 |
| `/rollback` | 弹出版本选择卡片 |
| `/backup restore <timestamp>` | 还原指定版本 |

## 工作原理

1. 备份：`tar + gzip` 压缩整个 openclaw 目录
2. 排除：`node_modules` / `.cache` / `backups` / `logs` / `media`
3. 还原前：自动备份当前状态到 `pre_rollback_<timestamp>.tar.gz`
4. 还原：`tar -xzf` 解压覆盖 → 重启Gateway

## 文件结构

```
openclaw-backup-rollback/
├── openclaw.plugin.json     # 插件元数据
├── SKILL.md                 # 本文档
└── scripts/
    ├── backup_openclaw.sh   # 备份脚本
    ├── rollback.py          # 回滚脚本
    └── backup_rollb_plugin.py  # 插件主入口
```

## 安装

```bash
clawhub install openclaw-backup-rollback
```

## 配置

无需配置，安装后自动生效。备份保存到 `~/.openclaw/backups/`。

## 依赖

- `tar`, `gzip` (系统自带)
- `systemctl` (systemd)
- Python 3 (用于回滚脚本)
