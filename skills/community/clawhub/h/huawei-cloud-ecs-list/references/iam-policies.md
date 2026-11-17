# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/cloudservers/detail` — `hcloud ECS ListServersDetails`
- SDK fallback: `huaweicloudsdkecs` v2 `EcsClient.list_servers_details` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `ecs:servers:list` | GET /v1/{project_id}/cloudservers/detail | List ECS servers |

`ecs:servers:list` was verified against the live IAM authorization schema
(`GetAuthorizationSchemaV5 --service_code=ecs`, cn-north-4, 2026-10-19); the
returned action set for ECS contains `ecs:servers:list` (read-only) and the
mutating actions `ecs:servers:create` / `delete` / `start` / `stop` / `reboot`
/ `rebuild` / `resize` / `update`, none of which this skill ever calls.

If you prefer a system policy, assign **ECSReadOnlyPolicy** instead of the
custom policy below. `ECSReadOnlyPolicy` was verified via
`ListPoliciesV5 --policy_type=system` (returns `ECSReadOnlyPolicy`,
`ECSCommonOperationsPolicy`, `ECSFullPolicy`).

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
3. Re-run `python3 scripts/list_ecs.py`.
