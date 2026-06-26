# Permissions

## 只读范围

| 命令 | 作用 |
|---|---|
| `jms_permissions.py list` | 查询授权规则列表 |
| `jms_permissions.py get` | 查询授权规则详情 |

## 组织要求

- 权限查询必须先有可用的 `JMS_ORG_ID`。
- 如果配置不完整，先 `config-status --json`，必要时 `config-write --confirm`。
- 如果当前没有组织上下文，先 `select-org`，再 `select-org --confirm`。
- 如果当前 `JMS_ORG_ID` 不可访问，重新 `select-org --confirm` 后再查。

## 示例

```bash
python3 scripts/jms_permissions.py list --filters '{"limit":20}'
python3 scripts/jms_permissions.py get --id <permission-id>
```

## 不支持

- `preview-create`
- `create`
- `preview-update`
- `update`
- `append`
- `preview-remove`
- `remove`
- `delete`
