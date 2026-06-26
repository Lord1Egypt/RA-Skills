# OpenClaw WebDAV Backup Skill

轻量级 OpenClaw 备份与恢复解决方案，支持本地打包、加密和 WebDAV 远程存储。

## 功能特性

- ✅ **全量/增量备份** - 支持多级增量备份策略
- ✅ **配置加密** - AES-256-CBC 加密敏感配置
- ✅ **WebDAV 上传** - 自动同步到远程存储
- ✅ **版本管理** - 列表查看、选择恢复、删除旧版本
- ✅ **保留策略** - 本地和远程自动清理旧备份
- ✅ **完整性检查** - 自动验证备份文件完整性
- ✅ **健康检查** - 诊断备份环境配置状态
- ✅ **Diff 预览** - 恢复前预览变更 (v1.2.0)
- ✅ **可移植导出** - 导出为可移植包，适配不同环境 (v1.2.0)
- ✅ **环境模板化** - IP/端口/路径等环境值抽成变量 (v1.2.0)
- ✅ **操作日志** - 结构化日志记录与审计 (v1.2.0)
- ✅ **SHA-256 校验** - 备份文件完整性校验 (v1.2.2)
- ✅ **压缩选项** - 支持 gzip/zstd (v1.2.2)
- ✅ **依赖预检** - 恢复前自动检查系统依赖 (v1.2.1)

## 快速开始

### 备份

```bash
# 全量备份
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh

# 增量备份（Smart 策略：周日全量，平日增量）
BACKUP_STRATEGY=smart bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh

# 加密 + WebDAV 上传
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --encrypt-config --upload

# 使用 zstd 压缩（更快，体积更小）
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --compress=zstd
```

### 恢复

```bash
# 列出所有版本
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --list

# 恢复最新版本
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --latest

# 恢复指定版本
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --from backups/openclaw/2026-04-02-030000

# 交互式选择
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh

# 检查依赖项（恢复前建议）
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --check-deps
```

### 删除

```bash
# 删除指定版本
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --delete 2026-04-01-030000

# 删除7天前的备份（dry-run 预览）
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --delete-old 7 --dry-run

# 实际删除
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --delete-old 7
```

### Diff 预览（v1.2.0 新增）

```bash
# 预览恢复变化
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --from <backup> --diff

# 详细对比
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --from <backup> --diff-format full

# 只看配置变化
bash skills/openclaw-webdav-backup/scripts/openclaw-diff.sh --from <backup> --config-only
```

### 可移植包导出（v1.2.0 新增）

导出为可移植包，适配不同部署环境：

```bash
# 基本导出
bash skills/openclaw-webdav-backup/scripts/openclaw-export.sh

# 导出到指定目录
bash skills/openclaw-webdav-backup/scripts/openclaw-export.sh --target ~/backups/

# 不模板化配置（保留原始值）
bash skills/openclaw-webdav-backup/scripts/openclaw-export.sh --no-sanitize
```

导出的包包含：
- `workspace/` - OpenClaw 工作区
- `extensions/` - 插件目录
- `config/openclaw.json.template` - 模板化配置文件
- `migrate.env.template` - 环境变量模板
- `scripts/migrate.sh` - 迁移脚本
- `scripts/check-compatibility.sh` - 兼容性检查
- `MIGRATION.md` - 迁移指南
- `manifest.json` - 清单文件

使用方式：
```bash
# 1. 解压
tar -xzf openclaw-portable-2026-04-03-063839.tar.gz
cd openclaw-portable-2026-04-03-063839

# 2. 检查兼容性
bash scripts/check-compatibility.sh

# 3. 配置环境
cp migrate.env.template .env
# 编辑 .env 填入实际值

# 4. 执行迁移
bash scripts/migrate.sh --env-file .env
```

### 健康检查

```bash
# 诊断备份环境配置
bash skills/openclaw-webdav-backup/scripts/openclaw-healthcheck.sh

# 检查内容包括：
# - 基础环境目录
# - 备份基础设施
# - 依赖命令（tar, curl, openssl）
# - 配置文件完整性
# - 现有备份文件完整性
```

## 备份策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `full` | 始终全量 | 小型工作区 |
| `weekly` | 每周全量 | 低频备份 |
| `daily` | 首次全量，后续增量 | 标准日备 |
| `smart` | 周日全量，平日增量 | 推荐生产环境 |
| `hourly` | 支持0→1→2多级增量 | 高频备份 |

## 目录结构

```
backups/openclaw/
├── .snapshots/
│   ├── level-0.snapshot
│   └── level-1.snapshot
├── 2026-04-02-030000/
│   ├── workspace.tar.gz
│   ├── extensions.tar.gz
│   ├── openclaw.json (或 .enc)
│   └── manifest.txt
└── 2026-04-01-030000/
    └── ...
```

## 配置

创建 `.env.backup`：
```bash
WEBDAV_URL="https://your-webdav-server/backup"
WEBDAV_USER="username"
WEBDAV_PASS="password"
REMOTE_KEEP=7
LOCAL_KEEP=7
```

创建 `.env.backup.secret`（加密密钥）：
```bash
BACKUP_ENCRYPT_PASS="your-secure-password"
```

## 定时任务

```cron
# Smart 策略：周日全量，周一到周六增量
0 0 * * 0 BACKUP_STRATEGY=smart /path/to/openclaw-backup.sh --encrypt-config --upload
30 3 * * 1-6 BACKUP_STRATEGY=smart /path/to/openclaw-backup.sh --encrypt-config --upload
```

## 文档

- [详细说明](SKILL.md)
- [定时配置](references/scheduling.md)
