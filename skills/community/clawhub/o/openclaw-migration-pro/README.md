# openclaw-migration-pro

> OpenClaw 一键迁移工具 - 数据永远在你手里

## 一句话介绍

像备份手机一样备份你的 OpenClaw，一键恢复、多设备同步、格式转换。

## 核心功能

| 功能 | 说明 | 命令 |
|------|------|------|
| **整机备份** | 备份所有数据 | `openclaw-migration-pro backup` |
| **整机恢复** | 从备份恢复 | `openclaw-migration-pro restore` |
| **导出 flomo** | 导出为 flomo 格式 | `openclaw-migration-pro export flomo` |
| **导出 Obsidian** | 导出为 Obsidian | `openclaw-migration-pro export obsidian` |
| **云同步** | Git/WebDAV 同步 | `openclaw-migration-pro sync` |

## 快速开始

### 安装

```bash
npx clawhub install openclaw-migration-pro
```

### 备份（在源电脑）

```bash
# 完整备份
openclaw-migration-pro backup --output ~/openclaw-backup/

# 选择性备份
openclaw-migration-pro backup --include memory --output ~/memory-backup/
```

### 恢复（在目标电脑）

```bash
# 完整恢复
openclaw-migration-pro restore --input ~/openclaw-backup/

# 选择性恢复
openclaw-migration-pro restore --include skills --input ~/backup/
```

### 导出为 flomo

```bash
openclaw-migration-pro export flomo --output flomo.jsonl
```

### 导出为 Obsidian

```bash
openclaw-migration-pro export obsidian --output ~/Obsidian-Vault/OpenClaw/
```

## 使用场景

### 场景 1: 换电脑

```bash
# 旧电脑：备份
openclaw-migration-pro backup --output ~/openclaw-backup/

# 复制到新电脑（U 盘/网盘/rsync）
rsync -av ~/openclaw-backup/ user@new-pc:~/

# 新电脑：恢复
openclaw-migration-pro restore --input ~/openclaw-backup/
```

### 场景 2: 多设备同步

```bash
# 配置 Git 同步
openclaw-migration-pro sync init --provider git --repo username/openclaw-data

# 推送
openclaw-migration-pro sync push

# 在另一台电脑拉取
openclaw-migration-pro sync pull
```

### 场景 3: 迁移到 flomo

```bash
# 导出
openclaw-migration-pro export flomo --output flomo.jsonl

# 上传到 flomo
# https://flomoapp.com/import
```

## 备份内容

| 目录 | 内容 | 大小 |
|------|------|------|
| `~/.openclaw/skills/` | 所有 Skills | ~10MB |
| `~/openclaw/workspace/` | Memory + 工作区 | ~50MB |
| `~/.openclaw/cron/` | Cron Jobs | ~1MB |
| `~/.openclaw/config/` | 配置文件 | ~100KB |

**总计**: ~61MB（压缩后 ~20MB）

## 命令行参考

### 备份

```bash
# 完整备份
openclaw-migration-pro backup --output ~/backup/

# 只备份 Memory
openclaw-migration-pro backup --include memory --output ~/memory-backup/

# 加密备份
openclaw-migration-pro backup --encrypt --password "secret" --output ~/encrypted/
```

### 恢复

```bash
# 完整恢复
openclaw-migration-pro restore --input ~/backup/

# 只恢复 Skills
openclaw-migration-pro restore --include skills --input ~/backup/
```

### 导出

```bash
# flomo 格式
openclaw-migration-pro export flomo --output flomo.jsonl

# Obsidian 格式
openclaw-migration-pro export obsidian --output ~/Obsidian-Vault/

# Notion 格式
openclaw-migration-pro export notion --output notion.md
```

## 与其他工具对比

| 功能 | openclaw-migration-pro | rsync | Git | 网盘 |
|------|-----------------|-------|-----|------|
| 一键备份 | ✅ | ❌ | ❌ | ❌ |
| 一键恢复 | ✅ | ❌ | ❌ | ❌ |
| 格式转换 | ✅ | ❌ | ❌ | ❌ |
| Cron 迁移 | ✅ | ❌ | ❌ | ❌ |
| Skills 迁移 | ✅ | ⚠️ | ⚠️ | ❌ |

## 故障排除

### 备份失败

```bash
# 检查磁盘空间
df -h ~

# 检查权限
ls -la ~/.openclaw/

# 重试
openclaw-migration-pro backup --force --output ~/backup/
```

### 恢复后 Skills 不可用

```bash
# 重新安装 Skills
openclaw-migration-pro restore --include skills --reinstall
```

## 最佳实践

### 定期备份

```bash
# 每天备份 Memory
0 2 * * * openclaw-migration-pro backup --include memory --output ~/daily-backup/$(date +\%Y-\%m-\%d)/

# 每周备份全部
0 3 * * 0 openclaw-migration-pro backup --output ~/weekly-backup/
```

### 多地备份

```bash
# 本地备份
openclaw-migration-pro backup --output ~/backup-local/

# 云盘备份
openclaw-migration-pro backup --output ~/Dropbox/openclaw-backup/

# Git 备份
openclaw-migration-pro sync push
```

## 许可证

MIT License

## 贡献

Issues and PRs welcome!

GitHub: https://github.com/your-org/openclaw-migration-pro
