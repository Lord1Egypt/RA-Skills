# IAM Policies — huawei-cloud-aom-list (read-only)

The skill only performs **read** queries against AOM (Application Operations
Management). Grant the smallest read-only permission set.

> **Verify before use:** Huawei Cloud IAM action names must be confirmed against
> an official source — the IAM schema query
> `hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=aom`,
> the official 《权限及授权项说明》 page for AOM, or the console policy picker.
> Do **not** assume the action names below are exhaustive for your account.

## Option 1 — System policy (simplest)

Attach the AOM read-only system policy to the user/agency (confirm the exact
policy name in the IAM console):

- `AOM ReadOnlyAccess` — read-only access to Application Operations Management.

The system policy is managed by Huawei Cloud and updated as new read APIs are
added.

## Option 2 — Least-privilege custom policy (IAM 5.0)

Scope the policy to exactly the read operations this skill uses. **Replace the
placeholder action list with the exact names returned by the IAM schema query
above** — do not copy unverified names.

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "<aom>:<resource>:list"
      ]
    }
  ]
}
```

The skill reads the following AOM resources (all `list`-type):

- 告警规则 / 告警规则模板 / 指标·事件告警规则
- 行动规则 / 静默规则
- 仪表盘 / 仪表盘分组
- 通知模板
- Prometheus 实例 / 接入码 / 服务发现规则

## Notes

- No write action (`*:create`, `*:update`, `*:delete`, `*:batch*`,
  `*:enable`, `*:disable`) is required — the skill refuses writes.
- The skill never stores or prints AK/SK; credentials come from the active
  hcloud profile or whitelisted environment variables.
- For cross-project / enterprise-project scoping, additionally constrain with a
  `Condition` (e.g. the enterprise project id) as your governance requires.