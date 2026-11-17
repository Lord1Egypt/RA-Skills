# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1.0/cdn/domains` — `hcloud CDN ListDomains`
- SDK fallback: `huaweicloudsdkcdn` v1 `CdnClient.list_domains` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `cdn:domain:list` | list | GET /v1.0/cdn/domains | Query the accelerated-domain list |

`cdn:domain:list` is the read-only list action for the CDN accelerated-domain
resource (as recorded in the Issue #52 spec / official CDN API reference; use
`IAM GetAuthorizationSchemaV5 --service_code=cdn` to confirm in your own
tenant).

If you prefer a system policy, assign **CDN ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cdn:domain:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问内容分发网络（CDN），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target account.
2. Grant `cdn:domain:list` (custom policy above) or the `CDN ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_cdn.py`.