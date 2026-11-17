# IAM Policies (least privilege, read-only)

The skill invokes exactly the read-only VPCEP list APIs (both execution paths):

- KooCLI `hcloud VPCEP ListEndpoints` — `GET /v1/{project_id}/vpc-endpoints`
- KooCLI `hcloud VPCEP ListEndpointService` — `GET /v1/{project_id}/vpc-endpoint-services`
- KooCLI `hcloud VPCEP ListServicePublicDetails` — `GET /v1/{project_id}/vpc-endpoint-services/public`
- SDK fallback: `huaweicloudsdkvpcep` `VpcepClient.list_endpoints` /
  `list_endpoint_service` / `list_service_public_details` (same REST paths)

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `vpcep:endpoints:list` | list | GET /v1/{project_id}/vpc-endpoints | Query the terminal endpoint list |
| `vpcep:endpointServices:list` | list | GET /v1/{project_id}/vpc-endpoint-services | Query endpoint services owned by the account |
| `vpcep:endpointServices:listPublic` | list | GET /v1/{project_id}/vpc-endpoint-services/public | Query public endpoint services |

These authorization actions belong to the **VPCEP (VPC 终端节点服务)** service.
The third action is required for `--view public`; without it the API returns
`common.01010013` / `not authorized`, which the script reports as an IAM 403
with a Chinese hint.

If you prefer a system policy, assign **VPCEP ReadOnlyAccess** instead of the
custom policy below (verify the exact system-policy name in the target region's
IAM console).

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "vpcep:endpoints:list",
        "vpcep:endpointServices:list",
        "vpcep:endpointServices:listPublic"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问终端节点服务（VPCEP），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project and region.
2. Grant the three list actions above (or the VPCEP read-only system policy).
3. Re-run `python3 scripts/list_vpcep.py --view endpoint --region <region>`.
4. For `--view public`, confirm `vpcep:endpointServices:listPublic` is granted —
   it is separate from the private service list action.
