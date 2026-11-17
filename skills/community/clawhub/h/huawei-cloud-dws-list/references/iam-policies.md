# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1.0/{project_id}/clusters` — `hcloud DWS ListClusters`
- SDK fallback: `huaweicloudsdkdws` v2 `DwsClient.list_clusters` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `dws:clusters:list` | GET /v1.0/{project_id}/clusters | List DWS clusters |

`dws:clusters:list` is the standard read-only action name used by the official
DWS read-only policy family (e.g. system policy **DWS ReadOnlyAccess**). If you
prefer a system policy, assign **DWS ReadOnlyAccess** instead of the custom
policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dws:clusters:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 DWS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `dws:clusters:list` (custom policy above) or the `DWS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_dws.py`.