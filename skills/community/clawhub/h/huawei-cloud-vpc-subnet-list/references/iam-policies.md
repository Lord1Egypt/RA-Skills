# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/subnets` — `hcloud VPC ListSubnets`
- SDK fallback: `huaweicloudsdkvpc` v2 `VpcClient.list_subnets` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `vpc:subnets:list` | list | GET /v1/{project_id}/subnets | Query the subnet list |

VPC subnets are a VPC-network resource: their authorization actions belong to
the **VPC** service and use the `subnets` resource type. The action above is the
least-privilege read-only permission for this single call.

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
        "vpc:subnets:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 VPC 子网（Subnet），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `vpc:subnets:list` (custom policy above) or the `VPC ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_subnet.py`.

> Note: under enterprise-project fine-grained authorization, ListSubnets
> requires the `vpc_id` filter; pass `--vpc-id` in that scenario so the request
> carries the project scope the policy expects.