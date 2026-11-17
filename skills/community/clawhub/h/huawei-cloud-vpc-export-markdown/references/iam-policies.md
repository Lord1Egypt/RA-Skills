# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/vpcs` — `hcloud VPC ListVpcs`
- SDK fallback: `huaweicloudsdkvpc` v2 `VpcClient.list_vpcs` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `vpc:vpcs:list` | list | GET /v1/{project_id}/vpcs | Query the VPC list for the Markdown report |

The report itself is written to the **local filesystem only** — no cloud write
permission is required or requested.

If you prefer a system policy, assign **VPC ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "vpc:vpcs:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问虚拟私有云（VPC），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `vpc:vpcs:list` (custom policy above) or the `VPC ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/export_vpc_markdown.py`.