# 默认同步范围与排除规则

说明：
- 这份文档只负责“默认范围、自定义范围、排除范围、恢复边界”
- 自动化接入顺序、cron、检查脚本示例，优先看 `automation.md`
- Nutstore / WebDAV 特有经验、排障顺序与使用注意事项，优先看 `nutstore-notes.md`

## 默认模式

没有特别说明时，脚本按默认模式执行。

## 默认同步范围

对每个 agent 工作区，默认仅同步以下内容：

### 1. 身份信息文件
- `AGENTS.md`
- `HEARTBEAT.md`
- `IDENTITY.md`
- `MEMORY.md`
- `SOUL.md`
- `TOOLS.md`
- `USER.md`

### 2. 记忆目录
- `memory/`

## 远端目录结构

按 agent 分目录：

```text
nutstore:/openclaw-backup/chief/
nutstore:/openclaw-backup/backend/
nutstore:/openclaw-backup/frontend/
nutstore:/openclaw-backup/openclawbot/
```

其中：
- 身份信息文件进入 `identity/`
- 记忆目录进入 `memory/`

例如：

```text
nutstore:/openclaw-backup/chief/identity/AGENTS.md
nutstore:/openclaw-backup/chief/memory/
```

## 自定义备份模式

如老板明确指定要备份哪些文件或目录，可通过 `CUSTOM_BACKUP_PATHS` 启用自定义备份模式。

示例：

```bash
CUSTOM_BACKUP_PATHS="docs/reports,memory/2026-04-19,TOOLS.md" \
AGENTS="chief" \
bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh
```

规则：
- 多个路径用英文逗号分隔
- 只接受 agent 工作区内的相对路径
- 文件会备份到 `nutstore:/openclaw-backup/<agent>/...`
- 目录会同步到 `nutstore:/openclaw-backup/<agent>/...`
- 未传 `CUSTOM_BACKUP_PATHS` 时，仍走默认模式

## 自定义恢复模式

如老板明确指定要恢复某个文件或目录，可使用：

```bash
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/2026-04-19/2026-04-19.md
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path docs/reports
```

规则：
- 第 3 个参数必须是 agent 工作区内的相对路径
- 文件会从 `nutstore:/openclaw-backup/<agent>/...` 定点恢复回本地对应路径
- 目录会从 `nutstore:/openclaw-backup/<agent>/...` 定点恢复回本地对应路径
- 不接受越界路径
- 若要做真实恢复验收，优先配合 `RESTORE_TARGET_ROOT` 恢复到测试目录，而不是直接覆盖正式工作区
- 如 `path` 模式目标是正式工作区，必须显式设置 `RESTORE_FORCE=1` 才允许执行

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

## 设计原则
1. 没有特别说明时，优先走默认模式
2. 先保证 agent 身份信息与记忆可恢复
3. 不同步敏感凭据与高频缓存
4. 按 agent 隔离备份，避免不同 agent 内容混放
5. 同步范围宁可保守，不默认放大到整个工作区
6. 如需自定义备份或自定义恢复，只在老板明确指定范围时启用
7. 做真实恢复验收时，优先恢复到测试目录，不直接覆盖正式工作区
8. `path` 模式恢复到正式工作区时，必须显式确认，不允许静默覆盖

补充：
- “为什么不把坚果云当运行盘”这类场景性说明，见 `nutstore-notes.md`
- “怎么接 cron / 怎么做检查”这类流程性说明，见 `automation.md`
