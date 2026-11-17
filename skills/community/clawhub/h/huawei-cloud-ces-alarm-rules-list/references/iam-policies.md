# IAM Policies — huawei-cloud-ces-alarm-rules-list

Least-privilege, **read-only** policy for inventorying CES alarm rules.

## Required permissions

Action names were **verified** against the CES authorization schema (no names are
invented):

```bash
hcloud IAM GetAuthorizationSchemaV5 --service_code=ces --cli-region=cn-north-4
```

| Action | Access level | 中文说明 | Used by |
|--------|--------------|----------|---------|
| `ces:alarms:list` | list | 授予查询告警规则列表的权限 | `ListAlarmRules`, v1 `ListAlarms` (状态补齐) |
| `ces:alarms:getPolicies` | read | 授予查询指定告警规则的策略列表权限 | `ListAlarmRulePolicies` |
| `ces:alarms:getResources` | read | 授予查询指定告警规则的资源列表权限 | `ListAlarmRuleResources` |
| `ces:alarms:getInstanceStatus` | read | 授予查询实例告警状态的权限 | 仅当环境的告警状态被单独拆权时需要 |

> Issue 正文里写的「`ces:alarm:*:list`」是权限族的概括写法。实测 schema 中不存在
> 通配形式，真实可达的 action 是上表中的 `ces:alarms:list` /
> `ces:alarms:getPolicies` / `ces:alarms:getResources`。授权时按真实 action 配置。

## IAM 5.0 identity policy (recommended)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ces:alarms:list",
        "ces:alarms:getPolicies",
        "ces:alarms:getResources"
      ]
    }
  ]
}
```

## Notes

- This skill performs **no** writes: the script refuses to construct
  `CreateAlarmRules` / `UpdateAlarmRulePolicies` / `DeleteAlarm` /
  `BatchEnableAlarmRules` / `AddAlarmRuleResources` and every other mutating
  operation, so no write action is needed.
- Scope the policy to the target account/region as required by your landing zone.
- Assign it to the IAM user / agency whose AK/SK the hcloud profile or the SDK
  environment uses. Never paste AK/SK into chat or command lines.
- A missing grant surfaces as a 403 (`AuthError`) with an explicit hint, never as
  a silently empty list.