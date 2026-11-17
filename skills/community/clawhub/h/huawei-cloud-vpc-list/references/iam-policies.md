# IAM Policies (least privilege, read-only)

The skill invokes exactly two Huawei Cloud OpenAPIs, both read-only (each has a
KooCLI path and an equivalent SDK fallback):

- KooCLI: `GET /v1/{project_id}/vpcs` — `hcloud VPC ListVpcs`
- SDK fallback: `huaweicloudsdkvpc` v2 `VpcClient.list_vpcs` (same REST path)
- KooCLI: `GET /v2.0/{project_id}/vpc/peerings` — `hcloud VPC ListVpcPeerings`
- SDK fallback: `huaweicloudsdkvpc` v2 `VpcClient.list_vpc_peerings` (same REST path)

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `vpc:vpcs:list` | list | GET /v1/{project_id}/vpcs | Query the VPC list |
| `vpc:peerings:list` | list | GET /v2.0/{project_id}/vpc/peerings | Query the VPC peering list |

VPC is a VPC-network resource: its authorization actions belong to the **VPC**
service and use the `vpcs` / `peerings` resource types. The actions above are
the least-privilege read-only permissions for the two calls.

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
        "vpc:vpcs:list",
        "vpc:peerings:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问虚拟私有云（VPC），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `vpc:vpcs:list` / `vpc:peerings:list` (custom policy above) or the
   `VPC ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_vpc.py` (or
   `python3 scripts/list_vpc.py --resource peering`).