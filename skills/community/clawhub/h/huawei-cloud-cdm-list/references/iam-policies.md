# IAM Policies — huawei-cloud-cdm-list

Least-privilege, **read-only** policy for querying the CDM cluster list and
cluster details.

## Required permissions

The CDM cluster-management read APIs require the `cdm:cluster:list` action
(ListClusters, 查询集群列表) and the `cdm:cluster:get` action
(ShowClusterDetail, 查询集群详情). Both actions belong to the CDM service
(DataArts Studio 权限管理文档列出 CDM 系统策略内含的 action 清单，其中查询类为
`cdm:cluster:get` / `cdm:cluster:list`；写类 action 如 `cdm:cluster:create` /
`cdm:cluster:delete` 等**不需要**，本 skill 也不应授予)。

## IAM identity policy (recommended, role-based authorization)

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cdm:cluster:list",
        "cdm:cluster:get"
      ]
    }
  ]
}
```

## Notes

- This skill performs **no** write operations, so no `cdm:cluster:create` /
  `cdm:cluster:delete` / `cdm:cluster:*:modify` action is needed — and the
  script additionally refuses to construct any mutating call.
- `cdm:cluster:list` covers `GET /v1.1/{project_id}/clusters` (ListClusters);
  `cdm:cluster:get` covers `GET /v1.1/{project_id}/clusters/{cluster_id}`
  (ShowClusterDetail). Assign both so the `--cluster-id` detail view works.
- Scope the policy to the target project/region as required by your landing
  zone; CDM is a project-level service (path parameter `project_id`).
- Assign the policy to the IAM user / agency whose AK/SK the hcloud profile or
  the SDK environment uses. Never paste AK/SK into chat or command lines.
- When an unauthorized call is made anyway, the service answers with an HTTP
  403 (没有操作权限), which the script classifies as an explicit
  `AuthError` hint pointing to this file.
