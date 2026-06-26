# Diagnose

## 入口职责

| 子命令 | 作用 | 是否写入 |
|---|---|---|
| `config-status` | 检查环境完整性 | 否 |
| `config-write` | 写入 `.env.local` | 是 |
| `ping` | 检查当前账号、连通性、可访问组织 | 否 |
| `select-org` | 列出或预览组织选择 | 否 |
| `select-org --confirm` | 持久化 `JMS_ORG_ID` | 是 |
| `resolve` | 解析对象 | 否 |
| `resolve-platform` | 解析平台 | 否 |
| `user-assets` | 查看用户可访问资产 | 否 |
| `user-nodes` | 查看用户可访问节点 | 否 |
| `user-asset-access` | 查看用户对某资产的账号/协议视图 | 否 |
| `recent-audit` | 快速查最近审计 | 否 |

## `select-org` 规则

- 不带 `--org-id` 时返回当前账号可访问组织列表。
- 带 `--org-id` 且不带 `--confirm` 时，只预览目标组织。
- 带 `--confirm` 时，把目标组织写回 `.env.local` 中的 `JMS_ORG_ID`。
- 若可访问组织集合恰好是 `{0002}` 或 `{0002,0004}`，业务查询路径允许自动写入 `0002`。

## 示例

```bash
python3 scripts/jms_diagnose.py config-status --json
python3 scripts/jms_diagnose.py config-write --payload '{"JMS_API_URL":"https://jump.example.com","JMS_USERNAME":"ops","JMS_PASSWORD":"secret"}' --confirm
python3 scripts/jms_diagnose.py ping
python3 scripts/jms_diagnose.py select-org
python3 scripts/jms_diagnose.py select-org --org-id <org-id> --confirm
```
