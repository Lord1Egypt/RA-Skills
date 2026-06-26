# Audit

## 支持的审计类型

| `audit-type` | 用途 |
|---|---|
| `operate` | 操作日志 |
| `login` | 登录日志 |
| `session` | 会话日志 |
| `command` | 命令审计 |

## 默认行为

- 未传 `date_from/date_to` 时，默认查询最近 7 天。
- 未传 `limit` 时，`list` 会自动翻页拉取当前时间窗内的全部结果。
- `audit-type=command` 时，`list` 和 `get` 都必须提供 `command_storage_id`。

## 常用命令

```bash
python3 scripts/jms_audit.py list --audit-type operate --filters '{"limit":30}'
python3 scripts/jms_audit.py list --audit-type login --filters '{"date_from":"2026-03-01 00:00:00","date_to":"2026-03-20 23:59:59"}'
python3 scripts/jms_audit.py get --audit-type command --id <command-id> --filters '{"command_storage_id":"<command-storage-id>"}'
```

## 查询摘要建议

| 维度 | 建议输出 |
|---|---|
| 时间范围 | 本次查询覆盖的时间窗 |
| 查询对象 | 用户、资产、节点、权限或组织 |
| 关键异常 | 重复失败、异常中断、敏感命令、权限扩大迹象 |
| 下一步 | 继续查哪个对象或继续缩小范围 |
