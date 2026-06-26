---
name: openclaw-backup
description: |
  自动备份 OpenClaw 整体配置到远程存储（支持任意 rclone 后端：COS、S3、FTP、SFTP、WebDAV等）。
  触发场景：
  - 创建/配置自动备份任务
  - 设置备份周期、保留份数、目标目录
  - 手动触发备份
  - 查看/恢复备份
  - OpenClaw 运行异常时的提醒
---

# OpenClaw 自动备份

## 功能特性

- ✅ 状态检查：异常时自动停止备份并提醒
- ✅ 完整备份：配置文件、skills、agents、workspace、memory、credentials
- ✅ 备份轮转：自动保留最新 N 份，删除旧备份
- ✅ 任意存储：支持 rclone 所有后端（S3/COS/FTP/SFTP/WebDAV等）
- ✅ 定时任务：支持 cron 定时自动备份

## 快速开始

### 1. 配置 rclone 远程存储（如已有可跳过）

```bash
# 查看现有配置
rclone listremotes

# 添加新配置（如腾讯COS）
rclone config create tencentcos s3 provider TencentCOS \
  access_key_id 你的AKID \
  secret_access_key 你的KEY \
  endpoint cos.ap-shanghai.myqcloud.com

# 添加其他存储（如S3、FTP等）
rclone config create mybackup s3 provider AWS access_key_id xxx secret_access_key xxx
rclone config create myftp ftp host ftp.example.com user myuser password mypass
```

### 2. 执行备份

```bash
/root/.openclaw/workspace-main/skills/openclaw-backup/scripts/backup.sh \
  --remote tencentcos:backup-1252695297/openclaw-backup \
  --keep 7
```

### 3. 配置定时任务

```bash
crontab -e
# 每天凌晨3点自动备份
0 3 * * * /root/.openclaw/workspace-main/skills/openclaw-backup/scripts/backup.sh \
  --remote tencentcos:backup-1252695297/openclaw-backup \
  --keep 7 >> /var/log/openclaw-backup.log 2>&1
```

## 备份内容

| 目录/文件 | 说明 | 默认 |
|-----------|------|------|
| openclaw.json | 主配置文件 | ✅ |
| openclaw.json.bak* | 配置文件历史 | ✅ |
| skills/ | 技能目录 (48个) | ✅ |
| agents/ | Agent配置 (6个) | ✅ |
| workspace* | 工作空间 (5个) | ✅ |
| memory/ | 全局记忆 | ✅ |
| credentials/ | 密钥凭证 | ✅ |
| config-backups/ | 配置备份 | ✅ |
| extensions/ | 插件扩展 | ❌ (太大) |

## 配置参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--remote` | ✅ | - | rclone 远程路径，格式：`remote:bucket/folder` |
| `--keep` | - | 7 | 保留的备份份数 |
| `--include-memory` | - | true | 是否包含 memory/ |
| `--include-config` | - | true | 是否包含配置文件和 skills |
| `--include-workspace` | - | true | 是否包含所有 workspace |
| `--include-credentials` | - | true | 是否包含 credentials |
| `--include-agents` | - | true | 是否包含 agents |
| `--include-extensions` | - | false | 是否包含 extensions（约836MB） |
| `--check-only` | - | false | 仅检查状态，不执行备份 |

## 常用示例

### 腾讯COS
```bash
--remote tencentcos:bucket-name/openclaw-backup
```

### 阿里云OSS
```bash
--remote aliyunoss:bucket-name/openclaw-backup
```

### AWS S3
```bash
--remote s3:bucket-name/openclaw-backup
```

### FTP/SFTP
```bash
--remote ftp:backup-folder
--remote sftp:backup-folder
```

### WebDAV
```bash
--remote webdav:backup-folder
```

## 检查状态

```bash
# 仅检查 OpenClaw 状态
/root/.openclaw/workspace-main/skills/openclaw-backup/scripts/backup.sh --check-only

# 查看远程备份
rclone lsl tencentcos:backup-1252695297/openclaw-backup/
```

## 恢复备份

```bash
# 1. 下载备份
rclone copy tencentcos:backup-1252695297/openclaw-backup/openclaw-backup-2026-03-25-161836.tar.gz /tmp/

# 2. 解压
cd /root/.openclaw
tar -xzf /tmp/openclaw-backup-2026-03-25-161836.tar.gz

# 3. 重启服务
openclaw gateway restart
```

## 依赖

- rclone 已配置远程存储
- openclaw CLI 可用

## ⚠️ 注意事项

1. **首次配置**：请先运行 `rclone config` 配置远程存储
2. **密钥凭证**：credentials/ 包含敏感信息，请妥善保管备份
3. **定时任务**：建议设置日志文件便于排查问题
4. **磁盘空间**：确保本地有足够空间临时存放备份文件（约3MB）