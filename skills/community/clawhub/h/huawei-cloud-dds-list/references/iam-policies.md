# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI, with one execution path
per tool:

| Tool | Command | SDK fallback | REST |
|------|---------|--------------|------|
| KooCLI | `hcloud DDS ListInstances` | huaweicloudsdkdds v3 `DdsClient.list_instances` | `GET /v3/{project_id}/instances` |

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | ----- | ------- | ------- |
| `dds:instance:list` (alias `dds:instance:listAll`) | list | GET /v3/{project_id}/instances | 查询数据库实例列表 |

`dds:instance:listAll` was verified against the official IAM authorization
schema (`hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4
--service_code=dds` → action `dds:instance:listAll`, `access_level: list`,
alias `dds:instance:list`, 中文描述「授予查询数据库实例列表的权限。」,
`resources: null` i.e. project-level, no resource-scope constraint). It is the
single read-only action this skill needs; `dds:instance:list` may be granted
instead when the account's policy uses the alias.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dds:instance:listAll"
      ],
      "Resource": "*"
    }
  ]
}
```

If your account already has a Huawei Cloud DDS read-only system policy
(e.g. DDS ReadOnlyAccess) assigned to the identity, that policy also covers
this call — confirm the exact policy name in the IAM console before relying on
it.

## 403 troubleshooting

If the script reports `无权限访问文档数据库服务（DDS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `dds:instance:listAll` (custom policy above) or the account's DDS
   read-only system policy.
3. Re-run `python3 scripts/list_dds.py`.

401 means the AK/SK itself is invalid or expired — refresh the credential
profile out-of-band; do not retry with a different identity.
