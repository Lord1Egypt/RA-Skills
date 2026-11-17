# IAM Policies (least privilege, read-only)

The skill invokes exactly four read-only Huawei Cloud OpenAPIs (KooCLI path and
SDK fallback use the same REST paths):

| `--resource` | API | REST path | IAM identity-policy action |
| ------------ | --- | --------- | -------------------------- |
| `projects` | `hcloud ProjectMan ListProjectsV4` | `GET /v4/projects` | none required (see note) |
| `repos` | `hcloud CodeArtsRepo ListProjectRepositories` | `GET /v4/projects/{project_id}/repositories` | `codeartsrepo:repository:getRepository` |
| `pipelines` | `hcloud CodeArtsPipeline ListPipelines` | `POST /v5/{project_id}/api/pipelines/list` | `codeartspipeline:pipeline:get` |
| `deploy-tasks` | `hcloud CodeArtsDeploy ListDeployTasks` | `GET /v2/{project_id}/tasks/list` | `codeartsdeploy:application:get` |

> Note: the `ListProjectsV4` API documentation states that the current API call
> requires no identity-policy permission; only a valid token / AK-SK is needed.

## Action provenance

The read actions were verified against the live IAM authorization schema on
2026-10-19 (region `cn-north-4`):

- `GetAuthorizationSchemaV5 --service_code=codeartsrepo` returns
  `codeartsrepo:repository:getRepository` (access_level `read`).
- `GetAuthorizationSchemaV5 --service_code=codeartspipeline` returns
  `codeartspipeline:pipeline:get` (access_level `read`).
- `GetAuthorizationSchemaV5 --service_code=codeartsdeploy` returns
  `codeartsdeploy:application:get` (access_level `read`).
- `GetAuthorizationSchemaV5 --service_code=projectman` returns no such schema
  (consistent with the API docs: no permission required for `ListProjectsV4`).

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codeartsrepo:repository:getRepository",
        "codeartspipeline:pipeline:get",
        "codeartsdeploy:application:get"
      ],
      "Resource": "*"
    }
  ]
}
```

If you prefer a system policy, assign the CodeArts Repo / Pipeline / Deploy
read-only system policies exposed in the IAM console for the target region.

## 403 troubleshooting

If the script reports `无权限访问 CodeArts，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant the read actions above (custom policy) or the corresponding read-only
   system policies.
3. Re-run `python3 scripts/list_codearts.py`.
