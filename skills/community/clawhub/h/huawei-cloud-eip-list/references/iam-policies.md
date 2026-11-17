# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v3/{project_id}/eip/publicips` — `hcloud EIP ListPublicips`
- SDK fallback: `huaweicloudsdkeip` v3 `EipClient.list_publicips` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `vpc:publicIps:list` | list | GET /v3/{project_id}/eip/publicips | Query the EIP (public IP) list |

EIP is a VPC-network resource: its authorization actions belong to the **VPC**
service and use the `publicIps` resource type. The action above is the
least-privilege read-only permission for this single call.

If you prefer a system policy, assign **EIP ReadOnlyAccess** (or
**VPC ReadOnlyAccess**) instead of the custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "vpc:publicIps:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问弹性公网IP（EIP），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `vpc:publicIps:list` (custom policy above) or the `EIP ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_eip.py`.