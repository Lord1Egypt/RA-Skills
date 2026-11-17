# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v3/{domain_id}/ccaas/cloud-connections` — `hcloud CC ListCloudConnections`
- SDK fallback: `huaweicloudsdkcc` v3 `CcClient.list_cloud_connections` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `cc:cloudConnections:list` | list | GET /v3/{domain_id}/ccaas/cloud-connections | Query the cloud connection list |

`cc:cloudConnections:list` was verified through the official IAM authorization
schema (`IAM GetAuthorizationSchemaV5 --service_code=cc`):

```json
{
  "name": "cc:cloudConnections:list",
  "access_level": "list",
  "description": {
    "en_US": "Grants permission to query the cloud connection list.",
    "zh_CN": "授予查询云连接列表权限。"
  },
  "resources": [
    { "urn_template": "cc::<account-id>:cloudConnection:<cloud-connection-id>", "required": true }
  ]
}
```

If you prefer a system policy, assign **CC ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cc:cloudConnections:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问云连接（CC），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `cc:cloudConnections:list` (custom policy above) or the
   `CC ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_cc.py`.
