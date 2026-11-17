# IAM Policies — huawei-cloud-ces-eps-query (read-only)

The skill only performs **read** queries against CES (Cloud Eye) and EPS
(Enterprise Project Service). Grant the smallest read-only permission set.

> **Verify before use:** Huawei Cloud IAM action names must be confirmed against
> an official source — the IAM schema query
> `hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=ces`
> (and `--service_code=eps`), the official 《权限及授权项说明》 pages, or the
> console's policy picker. Do **not** assume the action names below are
> exhaustive for your account.

## Option 1 — System policies (simplest)

Attach the read-only system policies to the user/agency:

- `CES ReadOnlyAccess` — read-only access to Cloud Eye.
- `EPS ReadOnlyAccess` — read-only access to Enterprise Project Service.

Both system policies are managed by Huawei Cloud and updated as new read APIs
are added.

## Option 2 — Least-privilege custom policy (IAM 5.0)

Scope the policy to exactly the read operations this skill uses. Replace the
action list with the exact names returned by the IAM schema query above.

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ces:alarms:list",
        "ces:alarmHistories:list",
        "ces:alarmTemplates:list",
        "ces:dashboards:list",
        "ces:notificationMasks:list",
        "ces:resourceGroups:list",
        "ces:oneClickAlarms:list",
        "eps:enterpriseProjects:list",
        "eps:enterpriseProjects:get",
        "eps:quotas:get",
        "eps:resources:list"
      ]
    }
  ]
}
```

## Notes

- No write action (`*:create`, `*:update`, `*:delete`, `*:enable`, `*:disable`,
  `*:migrate`, `*:batch*`) is required — the skill refuses writes.
- The skill never stores or prints AK/SK; credentials come from the active
  hcloud profile or whitelisted environment variables.
- For cross-project / enterprise-project scoping, additionally constrain with a
  `Condition` (e.g. `eps:ResourceTag/*` or the enterprise project id) as your
  governance requires.