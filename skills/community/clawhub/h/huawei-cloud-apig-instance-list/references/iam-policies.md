# IAM Policies (least privilege, read-only)

The skill invokes exactly two Huawei Cloud OpenAPI operations (both execution
paths):

- KooCLI: `GET /v2/{project_id}/apigw/instances` —
  `hcloud APIG ListInstancesV2 --cli-region=<region>`
- KooCLI: `GET /v2/{project_id}/apigw/instances/{instance_id}/apis` —
  `hcloud APIG ListApisV2 --cli-region=<region> --instance_id=<instance-id>`
- SDK fallback: `huaweicloudsdkapig` v2 `ApigClient.list_instances_v2` /
  `list_apis_v2` (same REST paths)

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `apig:instances:list` | list | GET /v2/{project_id}/apigw/instances | Query the dedicated instance list |
| `apig:apis:list` | list | GET /v2/{project_id}/apigw/instances/{instance_id}/apis | Query the API list of one instance |

Both actions are the least-privilege read-only permissions for these two
calls (APIG permission matrix —「查询专享版实例列表」and「查询API列表」).

If you prefer a system policy, assign **APIG ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apig:instances:list",
        "apig:apis:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 APIG 实例，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `apig:instances:list` and `apig:apis:list` (custom policy above) or
   the `APIG ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_apig_instances.py --region <region>`.

A 401 (`凭证无效`) means the AK/SK itself is invalid or expired — that is a
credential problem, not an IAM policy problem.