# IAM Policies (least privilege, read-only)

The skill invokes exactly two Huawei Cloud OpenAPI operations (both read-only
`GET`, across the CLI and SDK execution paths):

| Operation | REST path | IAM action |
| --------- | --------- | ---------- |
| `hcloud EIP ListBandwidths` / SDK `list_bandwidths` | `GET /v3/{project_id}/eip/bandwidths` | `eip:bandwidths:list` |
| `hcloud EIP ShowBandwidth` / SDK `show_bandwidth` | `GET /v3/{project_id}/eip/bandwidths/{bandwidth_id}` | `eip:bandwidths:get` |

`eip:bandwidths:list` and `eip:bandwidths:get` are the least-privilege
read-only permissions required by this skill. No write action (create / update
/ delete / change charge mode / bind or unbind a public IP) is needed or ever
requested.

If you prefer a system policy, assign **EIP ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "eip:bandwidths:list",
        "eip:bandwidths:get"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 EIP 带宽（Bandwidth），请检查 IAM 权限`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `eip:bandwidths:list` (list path) and `eip:bandwidths:get` (detail
   path), or the `EIP ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_bandwidths.py`.