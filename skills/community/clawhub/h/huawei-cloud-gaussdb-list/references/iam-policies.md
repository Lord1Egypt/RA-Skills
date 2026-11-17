# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v3/{project_id}/instances` — `hcloud GaussDB ListGaussMySqlInstances`
- SDK fallback: `huaweicloudsdkgaussdb` v3
  `GaussDBClient.list_gauss_my_sql_instances` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `gaussdb:instance:list` | GET /v3/{project_id}/instances | List GaussDB(for MySQL) instances |

`gaussdb:instance:list` is the standard read-only action name used by the
official GaussDB read-only policy family (e.g. system policy
**GaussDB ReadOnlyAccess**). If you prefer a system policy, assign
**GaussDB ReadOnlyAccess** instead of the custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "gaussdb:instance:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `gaussdb:instance:list` (custom policy above) or the
   `GaussDB ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_gaussdb.py`.