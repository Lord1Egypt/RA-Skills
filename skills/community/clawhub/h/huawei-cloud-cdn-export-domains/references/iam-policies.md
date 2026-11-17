# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1.0/cdn/domains` — `hcloud CDN ListDomains --cli-region=<region>`
- SDK fallback: `huaweicloudsdkcdn` v1 `CdnClient.list_domains` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `cdn:configuration:queryDomainList` | list | GET /v1.0/cdn/domains | Query the CDN accelerated-domain list for the export |

`cdn:configuration:queryDomainList` is the read-only action the CDN accelerator
control plane requires for the exported-domain query (confirmed against the live
CDN API 403 diagnostic: `is not authorized to perform: cdn:configuration:queryDomainList`).
Use `hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-1 --service_code=cdn`
to confirm the exact action name in your own tenant.

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
        "cdn:configuration:queryDomainList"
      ],
      "Resource": "*"
    }
  ]
}
```

The export file itself is written to the **local filesystem only** — no cloud
write permission is required or requested.

## 403 troubleshooting

If the script reports `无权限访问内容分发网络（CDN），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target account.
2. Grant `cdn:configuration:queryDomainList` (custom policy above) or the
   `CDN ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/export_cdn_domains.py`.