# IAM Policies (least privilege, read-only)

This skill invokes exactly four Huawei Cloud OpenAPI operations (both execution
paths use the same REST endpoints):

| Operation | REST path | Purpose |
| --------- | --------- | ------- |
| `ListEnterpriseRouters` | `GET /v3/{project_id}/enterprise-router/instances` | Enterprise router inventory |
| `ShowEnterpriseRouter` | `GET /v3/{project_id}/enterprise-router/instances/{er_id}` | Single ER detail |
| `ListVpcAttachments` | `GET /v3/{project_id}/enterprise-router/{er_id}/vpc-attachments` | VPC attachments of one ER |
| `ListRouteTables` | `GET /v3/{project_id}/enterprise-router/{er_id}/route-tables` | Route tables of one ER |

## Required IAM actions

Action names below were copied verbatim from
`hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=er`
(the official authorization schema), not inferred.

| Action | Access level | Used by |
| ------ | ------------ | ------- |
| `er:instances:list` | list | `ListEnterpriseRouters` |
| `er:instances:get` | read | `ShowEnterpriseRouter` |
| `er:instances:listVpcAttachments` | list | `ListVpcAttachments` |
| `er:routeTables:list` | list | `ListRouteTables` |

Related resource URN templates (from the same schema):

- `er:<region>:<account-id>:instances:<instance-id>`
- `er:<region>:<account-id>:routeTables:<route-table-id>`

The `er:instances:get` action also accepts the optional condition keys
`g:EnterpriseProjectId` and `g:ResourceTag/<tag-key>`.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "er:instances:list",
        "er:instances:get",
        "er:instances:listVpcAttachments",
        "er:routeTables:list"
      ],
      "Resource": [
        "er:*:*:instances/*",
        "er:*:*:routeTables/*"
      ]
    }
  ]
}
```

Replace `*` in the region / account segments with concrete values if your
organization requires tighter scoping (for example
`er:cn-north-4:<account-id>:instances/*`).

If you prefer a managed policy, assign the official **ER ReadOnlyAccess**
system policy instead of the custom policy above.

## 403 troubleshooting

If the script reports `无权限访问企业路由器（ER），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant the four actions above (or the `ER ReadOnlyAccess` system policy).
3. Re-run `python3 scripts/list_er.py --region cn-north-4`.

A real OpenAPI authorization error is returned by KooCLI as JSON on **stdout
with exit code 0** (for example `common.01010013 ... not authorized to perform:
er:instances:list`). The script detects that body and exits with code 1 instead
of reporting an empty list.