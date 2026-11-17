# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v2/products/service-types` — `hcloud BSS ListServiceTypes`
- SDK fallback: `huaweicloudsdkbss` v2 `BssClient.list_service_types`
  (same REST path, global endpoint)

## Required IAM permission

| Scope | API | Purpose |
| ----- | --- | ------- |
| BSS read-only (service-type catalog) | GET /v2/products/service-types | List the Huawei Cloud product / service catalog |

This call is a read-only catalog query under the BSS (费用中心) domain. The
**least-privilege** choice is the domain's **BSS ReadOnlyAccess** system policy.
If you author a custom policy instead, grant a read-only (`:list`) action on the
BSS service-type resource family — **verify the exact action / resource name in
the IAM console (权限及授权项说明) or with
`hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-1 --service_code=bss`
before production use**; do not assume the name below is final.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:*:list"
      ],
      "Resource": "*"
    }
  ]
}
```

> Prefer the **BSS ReadOnlyAccess** system policy when a broad wildcard is
> undesirable. Never grant BSS write actions (`*:create`, `*:delete`,
> `*:update`, `*:reclaim`, …) — this skill never issues them.

## 403 troubleshooting

If the script reports
`无权限访问华为云产品目录（BSS 云服务类型），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency with BSS access.
2. Grant the `BSS ReadOnlyAccess` system policy (or the custom read-only policy
   above).
3. Re-run `python3 scripts/list_products.py`.