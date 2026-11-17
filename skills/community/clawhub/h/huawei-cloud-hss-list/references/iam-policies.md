# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v5/{project_id}/host-management/hosts` — `hcloud HSS ListHostStatus`
- SDK fallback: `huaweicloudsdkhss` v5 `HssClient.list_host_status` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| ------ | ------------ | --- | ------- |
| `hss:host:listHostStatus` | list | GET /v5/{project_id}/host-management/hosts | Query the HSS protected-host list |

HSS is a Security service: its authorization actions belong to the **HSS**
service. The action above is the least-privilege read-only permission for this
single call. The exact action name was confirmed from the real 403 error
returned by `hcloud HSS ListHostStatus` when the action is missing:

```
User: iam::<account-id>:user:<name> is not authorized to perform:
hss:host:listHostStatus on resource: * because no identity-based policy allows
the hss:host:listHostStatus action.
```

If you prefer a system policy, assign **HSS ReadOnlyAccess** to cover all HSS
read operations.

## Custom least-privilege policy

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "hss:host:listHostStatus"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问主机安全服务（HSS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `hss:host:listHostStatus` (custom policy above) or the
   `HSS ReadOnlyAccess` system policy on the HSS service.
3. Re-run `python3 scripts/list_hss.py`.