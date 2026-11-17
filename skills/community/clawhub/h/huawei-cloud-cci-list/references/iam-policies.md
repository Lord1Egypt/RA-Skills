# IAM Policies (least privilege, read-only)

The skill invokes only the following Huawei Cloud CCI OpenAPI (Kubernetes-style
GET list operations) through KooCLI:

- `GET /api/v1/namespaces` — `hcloud CCI ListCoreV1Namespace`
- `GET /api/v1/pods` — `hcloud CCI ListCoreV1PodForAllNamespaces`
- `GET /api/v1/namespaces/{namespace}/pods` — `hcloud CCI ListCoreV1NamespacedPod`
- `GET /apis/apps/v1/deployments` — `hcloud CCI ListAppsV1DeploymentForAllNamespaces`
- `GET /apis/apps/v1/namespaces/{namespace}/deployments` — `hcloud CCI ListAppsV1NamespacedDeployment`

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `cci:namespace:list` | list | GET /api/v1/namespaces | Query the namespace list |
| `cci:pod:list` | list | GET /api/v1/pods; GET /api/v1/namespaces/{namespace}/pods | Query the pod / instance list |
| `cci:deployment:list` | list | GET /apis/apps/v1/deployments; GET /apis/apps/v1/namespaces/{namespace}/deployments | Query the workload (Deployment) list |

Verify the exact action names through the official IAM authorization schema
(query the CCI service code):

```bash
hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=cci
```

Also check the Huawei Cloud 《云容器实例(CCI) 权限及授权项说明》 document and
confirm the standard `service:resource_type:action` naming
(`cci:namespace:list`, `cci:pod:list`). If your tenant exposes a read-only
system policy for CCI (e.g. a CCI ReadOnlyAccess-style policy), assigning that
system policy is an equivalent alternative — confirm its exact name in IAM.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cci:namespace:list",
        "cci:pod:list",
        "cci:deployment:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问云容器实例（CCI），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant the read-only actions above (custom policy) or the CCI read-only system
   policy.
3. Re-run `python3 scripts/list_cci.py`.