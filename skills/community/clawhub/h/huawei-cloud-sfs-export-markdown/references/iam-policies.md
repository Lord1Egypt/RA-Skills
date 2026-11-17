# IAM Policies (least privilege, read-only)

This skill performs exactly one Huawei Cloud OpenAPI call (both execution
paths), then writes a Markdown file **locally**. It never writes to the cloud.

- KooCLI: `GET /v1/{project_id}/sfs-turbo/shares/detail` — `hcloud SFSTurbo ListShares`
- SDK fallback: `huaweicloudsdksfsturbo` v1 `SFSTurboClient.list_shares` (same REST path)

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `sfs:listShares` | GET /v1/{project_id}/sfs-turbo/shares/detail | List SFS Turbo file systems (for the Markdown export) |

`sfs:listShares` is the read-only action name for listing SFS Turbo file
systems. If you prefer a system policy, assign **SFS ReadOnlyAccess** instead of
the custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sfs:listShares"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 SFS，请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `sfs:listShares` (custom policy above) or the `SFS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_sfs_export_markdown.py`.

## Notes

- No write action (`sfs:createShare`, `sfs:deleteShare`, expand / shrink /
  mount / ACL ...) is required — the skill refuses such intents before anything
  runs.
- The generated `.md` file lives only on the local filesystem; no OBS / OMS /
  cloud-storage write permission is needed.
- The skill never stores or prints AK/SK; credentials come from the active
  hcloud profile or whitelisted environment variables.