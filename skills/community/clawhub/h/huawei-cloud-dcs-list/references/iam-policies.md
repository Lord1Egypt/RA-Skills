# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v2/{project_id}/instances` — `hcloud DCS ListInstances`
- SDK fallback: `huaweicloudsdkdcs` v2 `DcsClient.list_instances` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `dcs:instance:list` | GET /v2/{project_id}/instances | List DCS (Redis/Memcached) instances |

`dcs:instance:list` is the standard read-only action name used by the official
DCS read-only policy family (e.g. system policy **DCS ReadOnlyAccess**). If you
prefer a system policy, assign **DCS ReadOnlyAccess** instead of the custom
policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dcs:instance:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问分布式缓存服务（DCS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `dcs:instance:list` (custom policy above) or the `DCS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_dcs.py`.

## Least-privilege review checklist

Before granting access, verify each item:

- The credential belongs to the user or agency that owns the target project.
- The project id used by the SDK fallback resolves to the same project as the
  target region.
- The region is correct for the DCS endpoint being queried.
- Only `dcs:instance:list` is granted; no create, delete, resize, restart,
  flush or configuration actions are required.
- The policy resource is the intended project scope, not a broader wildcard
  than necessary.
- The same credential is not reused for unrelated mutating operations.

## Why only list is needed

The skill has a single execution path in both modes:

```text
KooCLI: hcloud DCS ListInstances
SDK:    DcsClient.list_instances
REST:   GET /v2/{project_id}/instances
```

If a request needs any other DCS action, the skill's write-intent guard rejects
it before execution. Granting additional DCS write actions therefore does not
add functionality to this skill.
