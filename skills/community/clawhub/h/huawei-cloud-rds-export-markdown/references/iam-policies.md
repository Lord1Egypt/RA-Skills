# IAM Policies (least privilege, read-only)

This skill performs exactly one Huawei Cloud OpenAPI call (both execution
paths), then writes a Markdown file **locally**. It never writes to the cloud.

- KooCLI: `GET /v3/{project_id}/instances` — `hcloud RDS ListInstances`
- SDK fallback: `huaweicloudsdkrds` v3 `RdsClient.list_instances` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `rds:instance:list` | GET /v3/{project_id}/instances | List RDS instances (for the Markdown export) |

`rds:instance:list` is the standard read-only action name used by the official
RDS read-only policy family (e.g. the system policy **RDS ReadOnlyAccess**). If
you prefer a system policy, assign **RDS ReadOnlyAccess** instead of the custom
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
3. Re-run `python3 scripts/list_rds_export_markdown.py`.

## Notes

- No write action (`rds:instance:create`, `rds:instance:delete`,
  `rds:instance:update`, resize / restart / restore ...) is required — the
  skill refuses such intents before anything runs.
- The generated `.md` file lives only on the local filesystem; no OBS / OMS /
  cloud-storage write permission is needed.
- The skill never stores or prints AK/SK; credentials come from the active
  hcloud profile or whitelisted environment variables.