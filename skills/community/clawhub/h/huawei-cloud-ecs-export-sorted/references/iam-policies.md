# IAM Policies (least privilege, read-only)

This skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/cloudservers/detail` — `hcloud ECS ListServersDetails`
- SDK fallback: `huaweicloudsdkecs` v2 `EcsClient.list_servers_details` (same REST path)

The report files (`.xlsx` / `.csv` / `.json`) are generated on the **local
machine only**; the local sort runs on the already-fetched result set. No ECS
write/delete API is ever invoked, so no write permission is needed or requested.

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `ecs:servers:list` | GET /v1/{project_id}/cloudservers/detail | List ECS servers |

`ecs:servers:list` is the standard read-only ECS list action (the ECS action set
also contains mutating actions `ecs:servers:create` / `delete` / `start` /
`stop` / `reboot` / `rebuild` / `resize` / `update`, none of which this skill
ever calls). If you prefer a system policy, assign **ECSReadOnlyPolicy**.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:servers:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 ECS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `ecs:servers:list` (custom policy above) or the `ECSReadOnlyPolicy`
   system policy.
3. Re-run `python3 scripts/list_ecs_export_sorted.py`.

> No write/delete actions are included — this skill never modifies resources and
> never writes the report back into the cloud.