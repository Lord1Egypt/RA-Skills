# IAM Policies (least privilege, read-only)

The skill invokes exactly one read-only Huawei Cloud OpenAPI (the KooCLI path
and the SDK fallback use the same REST path):

| API | REST path | IAM identity-policy action |
| --- | --------- | -------------------------- |
| `hcloud CSE ListEngines` | `GET /v2/{project_id}/enginemgr/engines` | `cse:engine:list` (access_level `list`, read) |

## Action provenance

Verified on 2026-11-09 in region `cn-north-4`:

- `GetAuthorizationSchemaV5 --service_code=cse` returns `cse:engine:list` with
  `access_level: list` (a read/list action).
- A live read-only call to `ListEngines` without the action returns the CSE
  OpenAPI error `SVCSTG.00509431` —
  `User is not authorized to perform: cse:engine:list` — confirming that
  `cse:engine:list` is the action the API checks.

The write actions in the same schema (`cse:engine:create`, `cse:engine:delete`,
`cse:engine:update`, `cse:engine:upgrade`, `cse:engine:resize`, ...) are **not**
granted and are never invoked by this skill.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cse:engine:list"
      ],
      "Resource": "*"
    }
  ]
}
```

If you prefer a system policy, assign a CSE read-only system policy from the
IAM console for the target region.

## 403 troubleshooting

If the script reports `无权限访问 CSE 微服务引擎，请检查 IAM 权限（cse:engine:list）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `cse:engine:list` (custom policy above) or a CSE read-only system
   policy.
3. Re-run `python3 scripts/list_cse_engines.py`.