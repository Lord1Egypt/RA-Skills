# 自动化接入建议

## 推荐顺序
1. 首次运行先完成初始化：确认 `bash` / `rclone` / WebDAV 连通 / 工作区目录正常
2. 手动验证 `rclone lsd nutstore:` 可用
3. 手动执行一次默认备份脚本
4. 先完成至少一次恢复 dry-run，最好再做一次恢复到测试目录的真实验收
5. 若有明确业务需要，再启用自定义备份
6. 最后接 cron 或上层任务流

说明：
- 这份文档只负责“接入顺序、自动化方式、执行示例”
- 默认/自定义同步边界与恢复边界，优先看 `storage-scope.md`
- Nutstore / WebDAV 特有注意事项，优先看 `nutstore-notes.md`

## 首次运行初始化建议

第一次使用时，建议严格按下面顺序执行：

```bash
# 1. 检查 rclone
rclone version

# 2. 初始化本地工作区根目录（如未设置）
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"

# 3. 进入某个 agent 工作区
cd "$WORKSPACE_ROOT/chief"

# 4. 初始化 nutstore remote
bash skills/nutstore-webdav-storage/scripts/config-rclone-nutstore.sh

# 5. 验证远端可用
rclone lsd nutstore:

# 6. 先做默认备份 dry-run
NUTSTORE_DRY_RUN=1 bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh

# 7. 再做一次正式默认备份
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh

# 8. 做一次默认恢复 dry-run
NUTSTORE_DRY_RUN=1 bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory
```

如需做真实恢复验收，优先恢复到测试目录：

```bash
RESTORE_TARGET_ROOT="$PWD/temp/nutstore-restore-test" \
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md
```

## AGENTS 选择建议

当前脚本默认 agent 集合为：

```bash
chief backend frontend openclawbot
```

### 默认全量执行
没有特别说明时，直接执行脚本即可：

```bash
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 只执行单个 agent
适合只处理当前 agent：

```bash
AGENTS="chief" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 只执行多个指定 agent
适合只处理部分 agent：

```bash
AGENTS="chief backend" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

### 与自定义模式组合
如只想让 `chief` 执行指定额外路径备份：

```bash
CUSTOM_BACKUP_PATHS="docs/reports,memory/2026-04-19" AGENTS="chief" \
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

说明：
- `AGENTS` 用空格分隔，不用逗号
- 未列入 `AGENTS` 的 agent 不会执行
- 建议默认模式稳定后，再叠加自定义路径范围

## cron 模板输出脚本

如需直接生成推荐 cron 模板，可执行：

```bash
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE_ROOT/chief"
bash skills/nutstore-webdav-storage/scripts/print-cron-examples.sh chief
```

说明：
- 默认输出 `chief` 的 cron 模板
- 也可传其他 agent 名称，如 `backend` / `frontend` / `openclawbot`
- 支持通过环境变量覆盖模板参数：`DEFAULT_CRON`、`CUSTOM_CRON`、`DEFAULT_LOG_NAME`、`CUSTOM_LOG_NAME`、`CUSTOM_PATHS_EXAMPLE`
- 仅在默认备份链路和恢复验收已经通过后，才建议正式启用 cron

## cron 示例

### 默认备份 cron

每天凌晨 2 点执行默认备份：

```cron
0 2 * * * cd "$HOME/.openclaw/workspace/chief" && bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh >> temp/nutstore-backup.log 2>&1
```

### 自定义备份 cron

仅在老板明确要求固定备份某些额外路径时再加：

```cron
30 2 * * * cd "$HOME/.openclaw/workspace/chief" && CUSTOM_BACKUP_PATHS="docs/reports,docs/decisions" AGENTS="chief" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh >> temp/nutstore-custom-backup.log 2>&1
```

自定义模式的远端路径与默认模式保持一致，仍然落在对应 agent 根目录下，例如：
- `docs/reports` → `nutstore:/openclaw-backup/chief/docs/reports`
- `docs/decisions` → `nutstore:/openclaw-backup/chief/docs/decisions`

## 轻量备份检查脚本

如需快速判断远端备份是否明显异常，可执行：

```bash
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE_ROOT/chief"
bash skills/nutstore-webdav-storage/scripts/check-nutstore-backup.sh chief
```

如需额外检查某个具体文件或目录是否已在远端存在：

```bash
bash skills/nutstore-webdav-storage/scripts/check-nutstore-backup.sh chief memory/YYYY-MM-DD/YYYY-MM-DD.md
bash skills/nutstore-webdav-storage/scripts/check-nutstore-backup.sh chief docs/reports
```

输出规则：
- `ok`：关键远端路径存在，检查通过
- `warn`：关键基础路径可用，但指定路径不存在或部分项缺失
- `error`：remote 不可访问、agent 根目录不存在、或存在不安全检查路径

退出码建议：
- `0`：全部通过
- `1`：存在警告
- `2`：存在错误

## cron 启用前检查清单

正式启用 cron 前，建议逐项确认：
1. `rclone lsd nutstore:` 已通过
2. 默认备份 dry-run 已通过
3. 默认正式备份已执行过至少一次
4. 至少一次恢复 dry-run 已通过
5. 日志目录已存在，如：`$WORKSPACE_ROOT/chief/temp`
6. 当前需要长期自动化的仅是默认模式；自定义模式只在明确需求稳定存在时再启用

## 恢复建议

恢复建议按 agent + scope 小范围执行；如需更细粒度恢复，可使用 path 模式。
更完整的恢复边界、`RESTORE_FORCE=1` 规则与设计原则，优先看 `storage-scope.md` 与 `nutstore-notes.md`。

最小示例：

```bash
cd "$WORKSPACE_ROOT/chief"

# 默认恢复
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief identity
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory

# path 恢复到正式工作区时需显式确认
RESTORE_FORCE=1 bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md

# 先做 dry-run
NUTSTORE_DRY_RUN=1 bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory
```

## 真实恢复验收建议

真实恢复验收优先恢复到测试目录，不直接覆盖正式工作区。
如需用 `path` 模式直接恢复到正式工作区，必须显式设置 `RESTORE_FORCE=1`。

示例：

```bash
cd "$WORKSPACE_ROOT/chief"
RESTORE_TARGET_ROOT="$PWD/temp/nutstore-restore-test" \
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md

# 如确需直接恢复到正式工作区，必须显式确认
RESTORE_FORCE=1 \
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md
```

验收重点：
1. 远端路径是否正确
2. 本地落点是否正确
3. 恢复后文件内容是否与源文件一致
4. 不影响正式工作区

补充：
- 如果比对失败，先不要直接判定脚本损坏
- 样本漂移、备份后源文件继续编辑等现象，见 `nutstore-notes.md`

## 与上层任务联动
适合在 `yuan-forum-sign` 日任务完成后再执行备份：
1. 先执行签到任务
2. 如有需要，先把本轮关键信息整理进入对应 agent 的 `memory/`
3. 没有特别说明时，执行默认备份脚本
4. 只有老板明确指定额外目录时，才启用 `CUSTOM_BACKUP_PATHS`
5. 当前默认不备份 `task-results`、secrets、cookies 等业务结果或敏感文件
