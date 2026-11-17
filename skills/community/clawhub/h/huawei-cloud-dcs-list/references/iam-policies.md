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
