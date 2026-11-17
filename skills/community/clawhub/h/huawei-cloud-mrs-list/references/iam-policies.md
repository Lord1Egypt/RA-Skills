# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI:

- `GET /v1.1/{project_id}/cluster_infos` — `hcloud MRS ListClusters`

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `mrs:cluster:list` | GET /v1.1/{project_id}/cluster_infos | List MRS clusters |

`mrs:cluster:list` is the standard read-only action name used by the official MRS
read-only policy family (e.g. `MRS ReadOnlyAccess`, verified via
`hcloud IAM ListPoliciesV5` / `GetPolicyVersionV5` during skill research). If you
prefer a system policy, assign **MRS ReadOnlyAccess** instead of the custom policy
below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "mrs:cluster:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `认证/授权失败（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `mrs:cluster:list` (custom policy above) or the `MRS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_mrs.py`.
