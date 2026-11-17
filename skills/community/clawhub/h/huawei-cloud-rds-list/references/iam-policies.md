# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v3/{project_id}/instances` — `hcloud RDS ListInstances`
- SDK fallback: `huaweicloudsdkrds` v3 `RdsClient.list_instances` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `rds:instance:list` | GET /v3/{project_id}/instances | List RDS instances |

`rds:instance:list` is the standard read-only action name used by the official
RDS read-only policy family (e.g. system policy **RDS ReadOnlyAccess**). If you
prefer a system policy, assign **RDS ReadOnlyAccess** instead of the custom
policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:instance:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 RDS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `rds:instance:list` (custom policy above) or the `RDS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_rds.py`.
