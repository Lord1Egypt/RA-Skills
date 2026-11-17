# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/cloudservers/{server_id}` — `hcloud ECS ShowServer`
- SDK fallback: `huaweicloudsdkecs` v2 `EcsClient.show_server` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `ecs:cloudServers:get` | GET /v1/{project_id}/cloudservers/{server_id} | Show one ECS server |

`ecs:cloudServers:get` is the ECS detail (show) action (alias
`ecs:servers:get`); it is read-only and distinct from the mutating actions
`ecs:cloudServers:create` / `delete` / `start` / `stop` / `reboot` / `rebuild`
/ `resize` / `update`, none of which this skill ever calls.

If you prefer a system policy, assign **ECSReadOnlyPolicy** instead of the
custom policy below. `ECSReadOnlyPolicy` is the official ECS read-only system
policy and is sufficient for this skill.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:cloudServers:get"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 ECS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `ecs:cloudServers:get` (custom policy above) or the `ECSReadOnlyPolicy`
   system policy.
3. Re-run `python3 scripts/show_ecs.py --instance-id <id>`.

## 404 troubleshooting

If the script reports `未找到该 ECS 实例`, the instance ID does not exist, was
deleted, or belongs to another region / project. Verify both the
`--instance-id` and `--region` values.