# IAM Policies (least privilege, read-only)

The skill invokes exactly the read-only DNS list APIs (both execution paths):

- KooCLI `hcloud DNS ListPublicZones` / `ListPrivateZones` — `GET /v2/zones`
- KooCLI `hcloud DNS ListRecordSets` — `GET /v2/recordsets`
- SDK fallback: `huaweicloudsdkdns` v2 `DnsClient.list_public_zones` /
  `list_private_zones` / `list_record_sets` (same REST paths)

## Required IAM actions

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `dns:zone:list` | list | GET /v2/zones | Query the public / private zone list |
| `dns:recordset:list` | list | GET /v2/recordsets | Query the record-set list (`--recordsets`) |

These authorization actions belong to the **DNS (云解析服务)** service and use
the `zone` / `recordset` resource types. They are the least-privilege read-only
permissions for the calls above.

If you prefer a system policy, assign **DNS ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dns:zone:list",
        "dns:recordset:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问云解析服务（DNS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `dns:zone:list` (and `dns:recordset:list` for `--recordsets`) with the
   custom policy above, or the `DNS ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_dns.py`.