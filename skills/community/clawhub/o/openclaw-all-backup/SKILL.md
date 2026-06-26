---
name: openclaw-backup
description: 完整备份 OpenClaw 配置目录 (.openclaw) 到同名带时间戳的目录，包括所有文件和隐藏文件。当用户需要备份 OpenClaw 配置、数据或创建配置快照时使用。
---

# OpenClaw Backup

完整拷贝 `.openclaw` 目录（包括所有文件和隐藏文件），新目录名自动附加年月日时分秒时间戳。

## 使用

### 快速备份

```bash
./scripts/openclaw-backup.sh
```

在 `~/.openclaw` 同级别目录创建 `.openclawYYYYMMDDHHMMSS` 备份。

### 示例

```
~/.openclaw              # 原始目录
~/.openclaw20260316010203 # 备份目录（自动创建）
```

## 备份内容（全部）

- `openclaw.json` - 主配置文件
- `openclaw.json.bak*` - 配置备份
- `workspace/` - 工作空间（含所有文件）
- `credentials/` - 凭据
- `extensions/` - 扩展插件
- `agents/` - Agent 数据
- `cron/` - 定时任务
- `completions/` - 自动补全数据
- `logs/` - 日志文件
- `.DS_Store` 等隐藏文件
- 所有其他文件

## 特点

- 保留文件权限、时间戳
- 包含隐藏文件（以点开头的文件）
- 使用 rsync（如有）或 cp -a 确保完整性

## 手动备份

```bash
# 获取时间戳
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# 创建目录并拷贝
mkdir -p ~/.openclaw${TIMESTAMP}
rsync -av ~/.openclaw/ ~/.openclaw${TIMESTAMP}/
```

## 恢复备份

```bash
# 重命名当前配置（谨慎操作）
mv ~/.openclaw ~/.openclaw.old

# 恢复备份
mv ~/.openclaw20260316010203 ~/.openclaw
```

## 脚本

- `scripts/openclaw-backup.sh` - 备份脚本
