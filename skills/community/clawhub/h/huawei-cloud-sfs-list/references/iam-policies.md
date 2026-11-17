# IAM Policies (least privilege, read-only)

The skill invokes exactly one SFS operation (both execution paths):

- KooCLI: `hcloud SFSTurbo ListShares` — GET `/v1/{project_id}/sfs-turbo/shares/detail`
- SDK fallback: `huaweicloudsdksfsturbo` v1 `SFSTurboClient.list_shares` (same operation)

Listing file systems is a read-only operation; no `create` / `delete` /
`expand` / `rename` / ACL / permission-rule action is ever called.

## Recommended system policy

Assign the **SFS Turbo ReadOnlyAccess** system policy to the IAM user or group
that owns the AK/SK used by hcloud/obsutil. This grants listing and inspection
without any write capability and requires no custom policy maintenance.

## Custom least-privilege policy

If a custom policy is preferred, scope it to the single listing action. The
exact action string MUST be confirmed against the official permission list
before use (see "Verify the action name" below).

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sfsturbo:shares:getAllShares"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

> The `Action` value above is the API-Explorer/authorization-item name for
> "获取文件系统列表"; the system policy name is the most reliable identifier.
> Confirm the exact literal with the command below — do **not** trust a
> hand-typed action name.

## Verify the action name (mandatory before applying a custom policy)

```bash
hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=sfsturbo
```

Copy the exact `name` / `urn_template` values from the response; do not
re-capitalize or normalize them. Alternatively, check the system policy:

```bash
hcloud IAM ListPoliciesV5 --cli-region=cn-north-4
hcloud IAM GetPolicyVersionV5 --cli-region=cn-north-4 --policy_id=<policy_id>
```

## 403 troubleshooting

If the script reports `无权限访问 SFS，请检查 IAM 权限`:

1. Confirm the AK/SK belongs to an IAM user in the target account and that the
   hcloud profile uses those credentials.
2. Grant the read-only listing action (system policy above) or the custom
   policy.
3. Re-run `python3 scripts/list_sfs.py`.

> No write/delete actions (create / delete / expand / ACL / permission rules)
> are included — this skill never modifies resources.