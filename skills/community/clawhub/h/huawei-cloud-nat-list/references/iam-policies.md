# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v2/{project_id}/nat_gateways` — `hcloud NAT ListNatGateways`
- SDK fallback: `huaweicloudsdknat` v2 `NatClient.list_nat_gateways` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `nat:natGateways:list` | list | GET /v2/{project_id}/nat_gateways | Query the public NAT gateway list |

The action above is the least-privilege read-only permission for this single
call (see the official NAT permission matrix
https://support.huaweicloud.com/api-natgateway/nat_api_0029.html —
「查询公网NAT网关列表 GET /v2/{project_id}/nat_gateways → nat:natGateways:list」).

If you prefer a system policy, assign **NAT ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "nat:natGateways:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问公网NAT网关，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `nat:natGateways:list` (custom policy above) or the
   `NAT ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_nat_gateways.py`.
