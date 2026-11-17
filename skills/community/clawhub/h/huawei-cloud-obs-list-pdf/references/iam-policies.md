# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OBS operation (both execution paths):

- KooCLI: `hcloud OBS ls` — obsutil-backed ListBuckets
- SDK fallback: `huaweicloudsdkobs` v1 `ObsClient.list_buckets` (same operation)

The PDF report is generated on the **local machine only**; no OBS write/delete
API is ever invoked, so no write permission is needed or requested.

## Required IAM action

| Action | API | Purpose |
| -------- | ----- | ------- |
| `obs:bucket:list` | GET / (ListBuckets) | List the account's OBS buckets |

`obs:bucket:list` is the standard read-only action for listing buckets. If you
prefer a system policy, assign **OBS ReadOnlyAccess** instead of the custom
policy below.

## Custom least-privilege policy

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "obs:bucket:list"
      ],
      "Resource": [
        "OBS:*:*:bucket:*"
      ]
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问 OBS，请检查 IAM 权限`:

1. Confirm the AK/SK belongs to an IAM user in the target account and that the
   obsutil config (`~/.obsutilconfig`) uses those credentials.
2. Grant `obs:bucket:list` (custom policy above) or the `OBS ReadOnlyAccess`
   system policy.
3. Re-run `python3 scripts/list_obs_buckets_pdf.py`.

> No write/delete actions (`obs:bucket:create`, `obs:bucket:delete`,
> `obs:object:put`, `obs:object:delete`, ...) are included — this skill never
> modifies resources and never writes into OBS.