# OpenList 自动化 Skill

本 Skill 用于让 AI Agent 通过 OpenList HTTP API 以可审计、可确认的方式执行常见操作：浏览路径、移动、重命名、单路径删除、创建离线任务，以及查询/取消任务。默认不支持覆盖写入、批量删除或其他高风险不可逆动作。

## 配置

必需环境变量：

- `OPENLIST_BASE_URL`：OpenList 根地址，例如 `http://localhost:5244` 或 `https://example.com/openlist`
- `OPENLIST_TOKEN`：OpenList Token 原文，请求头使用 `Authorization: <token>`，不要加 `Bearer`

可选环境变量：

- `OPENLIST_TIMEOUT_SECONDS`：默认 `30`
- `OPENLIST_VERIFY_TLS`：默认 `true`，自签名证书环境可设为 `false`
- `OPENLIST_AUDIT_PATH`：默认 `~/.codex/openlist/audit.jsonl`

支持从仓库根 `.env` 或 `skills/openlist/.env` 读取配置；环境变量优先级更高。请不要把 `.env` 提交到仓库。

## 命令清单

脚本入口：`python skills/openlist/scripts/openlist.py`

只读命令：

- `ping`
- `whoami`
- `fs-get --path <path>`
- `fs-list --path <dir> [--refresh]`
- `offline-tools`
- `task-info --task-type <move|offline_download> --tid <tid>`
- `task-list --task-type <move|offline_download> [--state undone|done]`
- `audit-show [--event-id <id>] [--plan-id <id>] [--tid <tid>]`

变更命令：

- `preview-move --src-path <path> --dst-dir <dir> [--conflict-policy fail|auto_rename|skip]`
- `preview-rename --path <path> --new-name <name> [--conflict-policy fail|auto_rename]`
- `preview-delete --path <path>`
- `preview-offline-create --url <url> [--url <url> ...] --dst-dir <dir> [--tool <tool>] [--delete-policy <policy>]`
- `apply --plan-file <file>`
- `task-cancel --task-type offline_download --tid <tid>`

## 两步确认

所有会修改状态的操作都必须走两步：

1. 先执行 `preview-*` 生成 `OperationPlan`
2. 用户确认后，再对同一份 plan 执行 `apply`

典型流程：

```powershell
python skills/openlist/scripts/openlist.py preview-move `
  --src-path "/from/report.pdf" `
  --dst-dir "/to/" `
  --json > move.plan.json

python skills/openlist/scripts/openlist.py apply --plan-file move.plan.json --json
```

`preview-* --json` 的 stdout 只输出单个 JSON 对象；`apply --json` 的 stdout 也只输出单个 JSON 对象。错误会保留在 stderr，方便 Agent 读取。

删除操作额外要求：

1. 只能先执行 `preview-delete`
2. Agent 必须向用户展示 **规范化后的精确路径** 与 **对象类型（file/dir）**
3. Agent 必须明确说明“删除不可逆”
4. 只有在用户明确确认后，才能对该 plan 执行 `apply`

## Move / Rename 示例

移动文件：

```powershell
python skills/openlist/scripts/openlist.py preview-move `
  --src-path "/from/report.pdf" `
  --dst-dir "/archive/" `
  --conflict-policy fail `
  --json > move.plan.json

python skills/openlist/scripts/openlist.py apply --plan-file move.plan.json --json
```

重命名文件：

```powershell
python skills/openlist/scripts/openlist.py preview-rename `
  --path "/archive/report.pdf" `
  --new-name "report-2026.pdf" `
  --json > rename.plan.json

python skills/openlist/scripts/openlist.py apply --plan-file rename.plan.json --json
```

冲突策略说明：

- `fail`：默认策略。发现同名冲突时只生成带冲突信息的 plan，`apply` 会拒绝执行
- `auto_rename`：自动生成稳定的新名称，例如 `report (1).pdf`
- `skip`：仅 `preview-move` 支持。目标已存在时，最终执行会跳过该项

无变更检测：

- 如果源条目已经位于目标目录，`preview-move` 会标记为 no-op
- 如果新名称与当前名称一致，`preview-rename` 会标记为 no-op
- no-op plan 的 `apply` 会返回成功并写审计，不会调用写接口

## 删除示例

预览删除：

```powershell
python skills/openlist/scripts/openlist.py preview-delete `
  --path "/archive/report.pdf" `
  --json > delete.plan.json
```

Agent 在执行 `apply` 前必须向用户明确展示：

- 规范化路径，例如 `/archive/report.pdf`
- 对象类型，例如 `file` 或 `dir`
- 删除不可逆，且该命令只允许删除单个显式路径

用户确认后执行：

```powershell
python skills/openlist/scripts/openlist.py apply --plan-file delete.plan.json --json
```

删除执行前会再次在线校验：

- 路径仍然存在
- 当前对象类型与 preview 时一致

任一条件不满足时，`apply` 会拒绝执行并提示重新 `preview-delete`。

## 离线任务示例

先查看可用工具：

```powershell
python skills/openlist/scripts/openlist.py offline-tools --json
```

预览创建任务：

```powershell
python skills/openlist/scripts/openlist.py preview-offline-create `
  --url "https://example.com/file.iso" `
  --dst-dir "/downloads/" `
  --json > offline.plan.json
```

执行并查询：

```powershell
python skills/openlist/scripts/openlist.py apply --plan-file offline.plan.json --json
python skills/openlist/scripts/openlist.py task-list --task-type offline_download --json
python skills/openlist/scripts/openlist.py task-info --task-type offline_download --tid "<tid>" --json
python skills/openlist/scripts/openlist.py task-cancel --task-type offline_download --tid "<tid>" --json
```

默认工具选择规则：

- 若实例启用了 `SimpleHttp`，优先选择 `SimpleHttp`
- 否则选择列表中的第一个工具
- 默认 `delete_policy=delete_never`

## 审计与回退指引

每一次 preview、apply、deny 和只读命令都会写入 JSONL 审计。默认位置：

```text
~/.codex/openlist/audit.jsonl
```

审计记录包含：

- `event_id`
- `timestamp`
- `phase`
- `request_id`
- `plan_id`
- `operation_type`
- `inputs`
- `outcome`

敏感字段如 `Authorization`、`token`、`password`、`secret` 会被脱敏。

查询示例：

```powershell
python skills/openlist/scripts/openlist.py audit-show --event-id "<event-id>" --json
python skills/openlist/scripts/openlist.py audit-show --plan-id "<plan-id>" --json
python skills/openlist/scripts/openlist.py audit-show --tid "<task-id>" --json
```

回退指引：

- move/rename 的 preview 和 apply 结果会给出反向操作建议
- offline task 会提示优先尝试 `task-cancel`
- delete 为不可逆操作，不提供回退指引

## 安全边界

- 不允许 `overwrite=true`
- 删除仅支持 `/api/fs/remove` 的单路径显式删除，不支持批量路径
- 不允许删除根目录 `/`
- `apply` 只允许执行白名单 endpoint：
  - `/api/fs/move`
  - `/api/fs/rename`
  - `/api/fs/remove`
  - `/api/fs/add_offline_download`
- 如果 plan 预检失败、仍有冲突或被手工篡改为危险字段，`apply` 会拒绝执行并写 `deny` 审计

## 常见排查

- 路径不存在：先执行 `fs-get` 或 `fs-list`
- 权限不足：确认 Token 是否具备对应目录或任务权限
- 同名冲突：重新 preview，并选择 `auto_rename` 或 `skip`
- 删除前对象发生变化：重新执行 `preview-delete`，再次确认路径与对象类型
- 看起来 HTTP 成功但结果仍失败：检查 JSON 中的 `openlist_code` 与 `message`
- 离线任务不可用：执行 `offline-tools`，确认实例已经启用下载工具
- TLS 失败或自签名证书：设置 `OPENLIST_VERIFY_TLS=false`
