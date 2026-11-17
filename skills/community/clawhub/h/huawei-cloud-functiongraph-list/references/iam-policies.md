# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v2/{project_id}/fgs/functions` — `hcloud functiongraph ListFunctions`
- SDK fallback: `huaweicloudsdkfunctiongraph` v2
  `FunctionGraphClient.list_functions` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `functiongraph:function:listFunctions` | GET /v2/{project_id}/fgs/functions | List FunctionGraph functions |

The action name was confirmed from the official IAM V5 authorization schema
(`hcloud IAM GetAuthorizationSchemaV5 --service_code=functiongraph` — the
`list`-level action `functiongraph:function:listFunctions`, 授予权限以查询函数列表).
If you prefer a system policy, assign **FunctionGraph ReadOnlyAccess** instead of
the custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "functiongraph:function:listFunctions"
      ],
      "Resource": "*"
    }
  ]
}
```

## Verify the action name officially

```bash
hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=functiongraph
```

## 403 troubleshooting

If the script reports `无权限访问 FunctionGraph，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `functiongraph:function:listFunctions` (custom policy above) or the
   `FunctionGraph ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_functiongraph.py`.
