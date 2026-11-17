# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v1/{project_id}/baremetalservers/detail` — `hcloud BMS ListBareMetalServers`
- SDK fallback: `huaweicloudsdkbms` v1 `BmsClient.list_bare_metal_servers` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `bms:server:list` | GET /v1/{project_id}/baremetalservers/detail | List BMS bare metal servers |

`bms:server:list` is the standard read-only action name used by the official BMS
read-only permission family. If you prefer a system policy, assign
**BMS ReadOnlyAccess** instead of the custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bms:server:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## Verify the action name officially

The action name above can be re-confirmed from the official authorization
schema (never infer it from naming patterns):

```bash
hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=bms
```

Copy the exact `name` / `urn_template` values returned for the list operation
and use them verbatim.

## 403 troubleshooting

If the script reports `无权限访问 BMS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `bms:server:list` (custom policy above) or the `BMS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_bms.py`.
