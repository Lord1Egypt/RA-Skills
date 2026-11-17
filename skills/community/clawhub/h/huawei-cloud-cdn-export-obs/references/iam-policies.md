# IAM Policies (least privilege)

The skill invokes exactly two Huawei Cloud OpenAPIs:

- CDN query (read-only): `GET /v1.0/cdn/domains` — `hcloud CDN ListDomains`
  (SDK fallback: `huaweicloudsdkcdn` v1 `CdnClient.list_domains`).
- OBS upload + read-back (write + read): `PUT /{object_key}` and
  `HEAD /{object_key}` — `hcloud OBS cp` / `hcloud OBS stat` (SDK fallback:
  `huaweicloudsdkobs` v1 `ObsClient.put_object` / `.head_object`).

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `cdn:domain:list` | list | GET /v1.0/cdn/domains | Query the accelerated-domain list |
| `obs:object:put` | write | PUT /{object_key} | Upload the exported result object |
| `obs:object:get` | read | HEAD /{object_key} | Read-back existence/size verification |

`cdn:domain:list` is the read-only list action for the CDN accelerated-domain
resource (confirm in your own tenant with
`IAM GetAuthorizationSchemaV5 --service_code=cdn`). For OBS, `obs:object:put` is
the object upload action and metadata read-back uses `obs:object:get` (the
`OBS ReadOnlyAccess` system policy covers the read but **not** the upload).

Least-privilege alternative: assign `CDN ReadOnlyAccess` + an OBS custom policy
that grants only `obs:object:put` / `obs:object:get` on the target bucket.

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
    },
    {
      "Effect": "Allow",
      "Action": [
        "obs:object:put",
        "obs:object:get"
      ],
      "Resource": [
        "obs:*:*:object:<bucket>/*"
      ]
    }
  ]
}
```

Replace `<bucket>` with the target bucket name used by `--bucket`.

## 403 troubleshooting

If the script reports `无权限访问...请检查 IAM 权限`:

1. Confirm the AK/SK belongs to a user / agency in the target account.
2. Grant `cdn:domain:list` for the query and `obs:object:put` (+
   `obs:object:get`) for the upload / read-back.
3. The KooCLI CDN path reads the active hcloud profile, while the OBS module
   reads the obsutil config — make sure both were configured for the same
   account out-of-band.