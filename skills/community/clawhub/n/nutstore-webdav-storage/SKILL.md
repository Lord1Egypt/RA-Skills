---
name: nutstore-webdav-storage
description: 使用坚果云 WebDAV 为 OpenClaw 多 agent 工作区做备份、归档与恢复的 skill。默认按 agent 备份身份信息文件与 memory 目录；如有明确要求，也支持自定义文件或目录备份到坚果云，并保留默认排除敏感文件的执行规则。
---

# nutstore-webdav-storage

用于把 **OpenClaw 多 agent 工作区** 里的身份信息文件与 `memory/` 目录同步到 **坚果云 WebDAV**。

## 技能定位

这是一个“备份/归档”型 skill，不是运行盘 skill。

统一口径：
- 本地仍是主存储
- 坚果云只做远端备份 / 归档 / 恢复源
- 远端按 agent 分目录
- 没有特别说明时，默认只备份各 agent 的身份信息文件与 `memory/`
- 如老板明确指定，可按 agent 执行自定义文件或目录备份
- 默认不同步 secrets、cookies、主密钥、虚拟环境、缓存目录

## 适用平台

适用的是**运行 OpenClaw 工作区的主机环境**，不是某个消息平台。

当前适用范围：
- Linux
- macOS
- WSL / 其他类 Unix shell 环境（满足 bash + rclone + WebDAV 连通时可用）

前提条件：
- 可执行 `bash`
- 已安装并可调用 `rclone`
- 可访问坚果云 WebDAV
- OpenClaw 工作区目录结构可用

说明：
- 该 skill 不依赖 QQ / Telegram / Discord 等消息平台本身
- 无论从哪个聊天入口触发，最终都必须在满足上述条件的主机上执行
- 当前不按“原生适配”定义纯 Windows CMD/PowerShell 环境，也不面向纯移动端执行环境

## 默认路径

### 本地源目录
默认使用 OpenClaw 工作区根目录：
```text
$WORKSPACE_ROOT
```

首次运行时，如当前环境还没有明确工作区根目录，建议先初始化：
```bash
export WORKSPACE_ROOT="$HOME/.openclaw/workspace"
```

如你的 OpenClaw 工作区不在默认位置，请改成你自己的实际路径。

### 远端目标目录
默认坚果云远端目录：
```text
nutstore:/openclaw-backup
```

目录结构按 agent 分开，例如：
```text
nutstore:/openclaw-backup/chief/
nutstore:/openclaw-backup/backend/
nutstore:/openclaw-backup/frontend/
nutstore:/openclaw-backup/openclawbot/
```

可按需覆盖。

## 快速决策

### 0）第一次使用，想先完成初始化
读：本页“首次运行初始化说明”，再按需继续看 `references/rclone-setup.md`

### 1）想先完成坚果云连接配置
读：`references/rclone-setup.md`

如需了解坚果云 / WebDAV 场景下的使用边界、排障顺序和恢复验收注意事项，再读：`references/nutstore-notes.md`

### 2）没特别说明，想直接做一次默认备份
用：`scripts/backup-openclaw-to-nutstore.sh`

### 3）老板明确指定了要备份的文件或目录
用：`CUSTOM_BACKUP_PATHS` + `scripts/backup-openclaw-to-nutstore.sh`

### 4）想恢复默认范围（identity / memory）
用：`scripts/restore-openclaw-from-nutstore.sh`

### 5）想恢复老板明确指定的某个文件或目录
用：`scripts/restore-openclaw-from-nutstore.sh <agent> path <relative-path>`

说明：
- 如 `path` 模式目标是正式工作区，必须显式设置 `RESTORE_FORCE=1`
- 如只是做恢复验收，优先设置 `RESTORE_TARGET_ROOT` 到测试目录

### 6）想生成 cron 模板
用：`scripts/print-cron-examples.sh`

### 7）想快速检查远端备份是否正常
用：`scripts/check-nutstore-backup.sh [agent] [optional-relative-path]`

### 8）想看默认同步/排除范围与自定义规则
读：`references/storage-scope.md`

### 9）想看坚果云 / WebDAV 特有注意事项
读：`references/nutstore-notes.md`

## 默认同步范围
对每个 agent，没有特别说明时默认同步：
- 身份信息文件：`AGENTS.md`、`HEARTBEAT.md`、`IDENTITY.md`、`MEMORY.md`、`SOUL.md`、`TOOLS.md`、`USER.md`
- `memory/`

## AGENTS 用法

默认情况下，如不显式传入 `AGENTS`，脚本会按默认集合执行：

```bash
chief backend frontend openclawbot
```

### 1）默认全量 agent
适合：没有特别说明时，按默认范围做整套备份。

```bash
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 2）只跑单个 agent
适合：只想处理当前 agent，例如只备份 `chief`。

```bash
AGENTS="chief" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 3）只跑多个指定 agent
适合：只处理部分 agent，而不是默认全量。

```bash
AGENTS="chief backend" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

说明：
- `AGENTS` 使用空格分隔，不用逗号
- 未在 `AGENTS` 中列出的 agent，本轮不会执行
- `CUSTOM_BACKUP_PATHS` 与 `AGENTS` 可同时组合使用

## 自定义备份范围
如老板明确指定文件或目录，可通过 `CUSTOM_BACKUP_PATHS` 传入相对路径列表，按 agent 备份到与默认模式一致的远端目录结构下。

示例：
```bash
CUSTOM_BACKUP_PATHS="docs/reports,memory/2026-04-19,TOOLS.md" \
AGENTS="chief" \
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

示例对应远端位置：
- `docs/reports` → `nutstore:/openclaw-backup/chief/docs/reports`
- `memory/2026-04-19` → `nutstore:/openclaw-backup/chief/memory/2026-04-19`
- `TOOLS.md` → `nutstore:/openclaw-backup/chief/TOOLS.md`

说明：
- 多个路径用英文逗号分隔
- 路径必须是 agent 工作区内的相对路径
- 文件会备份到 `nutstore:/openclaw-backup/<agent>/...`
- 目录会整体同步到 `nutstore:/openclaw-backup/<agent>/...`
- 未显式传入 `CUSTOM_BACKUP_PATHS` 时，仍走默认备份模式

## 默认排除范围
- 默认模式下，除身份信息文件与 `memory/` 之外的其他业务文件
- 自定义模式下，未被明确指定的其他业务文件
- `**/secrets/**`
- `**/cookies/**`
- `**/.secret.key`
- `**/.venv/**`
- `**/.conda-env/**`
- `**/node_modules/**`
- `temp/`
- 其他缓存或敏感目录

## 工作规则
1. 优先使用 `rclone` + WebDAV，不把登录密码直接写进脚本。
2. 统一使用应用密码，不使用账号登录密码。
3. 先配置远端，再执行备份/恢复脚本。
4. 未经老板明确要求，不把 secrets、cookies、主密钥同步到坚果云。
5. 远端统一按 agent 分目录管理，不把多个 agent 内容混在一起。
6. 没有特别说明时，默认只备份身份信息文件与 `memory/`；其他目录需要老板明确要求才扩展。
7. 如启用自定义备份，只允许传 agent 工作区内的相对路径，不接受越界路径。
8. 备份前优先确认目标目录；恢复前优先确认是否允许覆盖本地文件。
9. 自动化调用优先走脚本，不重复手写一长串 `rclone` 命令。

## 首次运行初始化说明

第一次使用时，不要直接上 cron，先按下面顺序完成主链路验证：

1. 确认执行环境：`bash`、`rclone`、WebDAV 连通、工作区目录正常
2. 初始化远端：`bash skills/nutstore-webdav-storage/scripts/config-rclone-nutstore.sh`
3. 验证远端：`rclone lsd nutstore:`
4. 先跑默认备份（必要时先 `NUTSTORE_DRY_RUN=1`）
5. 至少完成一次恢复 dry-run
6. 如需真实恢复验收，优先设置 `RESTORE_TARGET_ROOT` 恢复到测试目录
7. 默认模式稳定后，再决定是否启用自定义模式或 cron

最小示例：
```bash
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE_ROOT/chief"

bash skills/nutstore-webdav-storage/scripts/config-rclone-nutstore.sh
rclone lsd nutstore:
NUTSTORE_DRY_RUN=1 bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
NUTSTORE_DRY_RUN=1 bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory
```

如需详细初始化、cron 与恢复验收说明，读：`references/automation.md`
如需看 Nutstore / WebDAV 场景注意事项，读：`references/nutstore-notes.md`

## 推荐工作流

### 默认备份
```bash
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 单 agent / 多 agent 备份
```bash
AGENTS="chief" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
AGENTS="chief backend" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 自定义备份
```bash
CUSTOM_BACKUP_PATHS="docs/reports,memory/2026-04-19,TOOLS.md" AGENTS="chief" \
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 默认恢复
```bash
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief identity
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory
```

### 定点恢复
```bash
RESTORE_FORCE=1 bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/2026-04-19/2026-04-19.md
RESTORE_TARGET_ROOT="$PWD/temp/nutstore-restore-test" \
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/2026-04-19/2026-04-19.md
```

### 自动化 / 检查
```bash
bash skills/nutstore-webdav-storage/scripts/print-cron-examples.sh chief
bash skills/nutstore-webdav-storage/scripts/check-nutstore-backup.sh chief
```

## 环境变量
脚本支持以下环境变量覆盖默认值：

- `NUTSTORE_REMOTE`：默认 `nutstore:/openclaw-backup`
- `WORKSPACE_ROOT`：默认 `$HOME/.openclaw/workspace`
- `OPENCLAW_ROOT`：兼容旧变量名，仅作为 `WORKSPACE_ROOT` 的回退来源
- `RESTORE_TARGET_ROOT`：恢复目标根目录；默认与 `WORKSPACE_ROOT` 一致，可覆盖到测试目录做安全验收
- `RCLONE_BIN`：默认 `rclone`
- `NUTSTORE_DRY_RUN`：设为 `1` 时执行 `--dry-run`
- `AGENTS`：默认 `chief backend frontend openclawbot`
- `CUSTOM_BACKUP_PATHS`：可选，自定义备份相对路径列表，多个路径用英文逗号分隔；远端路径与默认模式保持同一套 agent 根目录结构

## 何时读附加参考
- 配置失败 / 首次配置 → `references/rclone-setup.md`
- 想调整默认同步范围或查看自定义备份/恢复规则 → `references/storage-scope.md`
- 想接 cron / 自动化，或做真实恢复验收 → `references/automation.md`
- 想看 Nutstore / WebDAV 特有边界、排障顺序、恢复注意事项 → `references/nutstore-notes.md`
- 想直接生成推荐 cron 模板 → `scripts/print-cron-examples.sh`
- 想快速检查远端备份状态 → `scripts/check-nutstore-backup.sh`
