# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (on both execution paths):

- KooCLI: `GET /v1/{project_id}/cloudservers/detail` — `hcloud ECS ListServersDetails`
- SDK fallback: `huaweicloudsdkecs` v2 `EcsClient.list_servers_details` (same REST path)

The Markdown report is written to the **local filesystem only** — no ECS write
API is ever called, so no write IAM action is required.

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `ecs:servers:list` | GET /v1/{project_id}/cloudservers/detail | List ECS instances of the project |

`ecs:servers:list` is the standard read-only action used by the official ECS
read-only policy family. If you prefer a system policy, assign
**ECSReadOnlyPolicy** (or `ECS ReadOnlyAccess`) instead of the custom policy
below.

## Custom least-privilege policy (IAM 5.0)

The action name and version below follow the official ECS authorization schema
(ECS 权限及授权项说明). Do not re-capitalize or normalize them.

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

If the script reports `无权限访问弹性云服务器（ECS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `ecs:servers:list` (custom policy above) or the `ECSReadOnlyPolicy`
   system policy.
3. Re-run `python3 scripts/list_ecs_export_markdown.py`.

A `401` means the AK/SK itself is invalid or expired — re-configure credentials
out-of-band and re-run; never paste AK/SK into a chat.