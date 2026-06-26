# 审计与调查

## 快速概览

- 开始前先到 [runtime.md](runtime.md) 判断本次是“首次全量校验”还是“后续轻量校验”。
- 主入口：`python3 scripts/jumpserver_api/jms_query.py <subcommand> ...`
- 支持子命令：`audit-list`、`audit-get`、`terminal-sessions`、`command-storage-hint`、`audit-analyze`、`capabilities`。
- 调查分析类请求统一使用这份文档，无需额外 playbook。
- 未选组织时，先通过 `python3 scripts/jumpserver_api/jms_diagnose.py select-org --org-id <org-id> --confirm` 选择组织；只有 `{0002}` 或 `{0002,0004}` 环境会自动写入 `0002`。
- `audit-list` 默认按当前时间窗自动翻页拉全量；显式传 `limit` / `offset` 时按分页结果返回。
- 未传 `date_from/date_to` 时，`audit-list/audit-analyze/terminal-sessions` 默认查询最近 7 天。
- 当环境存在多个 `command storage` 时，`command-record-query` 与 `high-risk-command-audit` 在普通查询场景下会优先使用默认 storage 或单个可用 storage 继续查询，并在结果里提示还可以切换到哪些 storage；只有在存在多个 storage 且无法推导默认 storage 时，才会阻塞并要求显式指定 `command_storage_id`。
- 当 filters 显式传入 `command_storage_scope=all` 且未指定 `command_storage_id` 时，这两个能力会遍历全部可访问 command storage 并合并汇总结果；该模式优先用于报告/使用分析场景。
- 命令审计在大时间窗下可能遇到存储侧 429 限流；优先缩小时间窗、分段查询，或先确认正确的 `command_storage_id`。

## `audit-type` 对应场景

| `audit-type` | 适用场景 | 备注 |
|---|---|---|
| `operate` | 资源变更、权限变更、配置操作 | 适合直接查操作日志 |
| `login` | 登录成功、登录失败、锁定、认证异常 | 适合排查异常来源和失败登录 |
| `session` | 审计侧会话记录 | 适合查访问行为与时长 |
| `terminal-session` | terminal 侧在线/历史会话明细 | 适合查当前在线连接和会话结束状态 |
| `ftp` | 文件上传、下载、SFTP 传输 | 适合文件传输审计 |
| `command` | 会话中的命令记录 | 适合高危命令审计和命令关键字排查 |

## `audit-analyze --capability` 适用场景

| 能力 | 适用问题 |
|---|---|
| `command-record-query` | 按用户/资产/关键字排查命令 |
| `high-risk-command-audit` | 排查高危命令、拒绝命令 |
| `session-record-query` | 查会话明细、协议、状态 |
| `file-transfer-log-query` | 查文件上传/下载记录 |
| `abnormal-hours-login-query` | 查异常时间段登录 |
| `abnormal-source-ip-login-query` | 查异常来源 IP 登录 |
| `failed-login-statistics` | 统计失败登录排行 |
| `privileged-account-usage-audit` | 审计特权账号使用情况 |
| `session-behavior-statistics` | 汇总会话行为统计 |
| `frequent-operation-user-ranking` | 统计高频操作用户排行 |
| `suspicious-operation-summary` | 跨命令、登录、会话、传输汇总可疑行为 |
| `user-session-analysis` / `asset-session-analysis` | 从用户或资产维度分析会话行为 |

## 高频示例

最近操作日志：

```bash
python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type operate --filters '{"limit":5}'
```

`terminal-sessions` 补充说明：

- 传 `asset` 时，会先尝试把资产名解析为 `asset_id` 再请求 terminal session 接口。
- 当前实现会自动去掉 terminal session 不稳定的 `days` 服务端参数，只保留本地时间窗换算后的 `date_from/date_to`。
- 若按资产的服务端过滤没有命中，会自动退回到“拉宽列表后本地按资产过滤”，并在 `summary.filter_strategy` 标明 `local_asset_fallback`。
- 每条记录都带 `asset_evidence`，可直接用于说明为什么判定该记录属于目标资产。
- 如果目标会话发生在更早时间，请显式传 `days` 或 `date_from/date_to`。

最近登录审计：

```bash
python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type login --filters '{"limit":5}'
python3 scripts/jumpserver_api/jms_query.py terminal-sessions --view online
python3 scripts/jumpserver_api/jms_query.py terminal-sessions --view history --filters '{"limit":5}'
```

高危命令审计：

```bash
python3 scripts/jumpserver_api/jms_query.py command-storage-hint
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability high-risk-command-audit --filters '{"date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59","command_storage_id":"<storage-id>"}'
```

文件传输审计：

```bash
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability file-transfer-log-query --filters '{"direction":"upload","date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59"}'
```

命令记录查询（多 storage 环境会优先使用默认 storage，并提示可切换 storage）：

```bash
python3 scripts/jumpserver_api/jms_query.py command-storage-hint
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability command-record-query --filters '{"date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59","command_storage_id":"<storage-id>"}'
```

报告/使用分析场景汇总全部 command storage：

```bash
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability command-record-query --filters '{"date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59","command_storage_scope":"all"}'
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability high-risk-command-audit --filters '{"date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59","command_storage_scope":"all"}'
```

可疑行为汇总：

```bash
python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability suspicious-operation-summary --filters '{"days":7,"user":"openclaw"}'
```
