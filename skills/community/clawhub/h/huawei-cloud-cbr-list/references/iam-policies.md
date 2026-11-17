# IAM Policies (least privilege, read-only)

The skill invokes exactly one CBR operation (both execution paths):

- KooCLI: `hcloud CBR ListBackups` — GET `/v3/{project_id}/backups`
- SDK fallback: `huaweicloudsdkcbr` v1 `CbrClient.list_backups` (same operation)

Listing backups is a read-only operation; no `create` / `delete` / `restore` /
`copy` / `import` / `replicate` / `update` action is ever called.

## Recommended system policy

Assign the **CBR ReadOnlyAccess** system policy to the IAM user or group that
owns the AK/SK used by hcloud. This grants listing and inspection without any
write capability and requires no custom policy maintenance.

## Custom least-privilege policy

If a custom policy is preferred, scope it to the single listing action:

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cbr:backup:list"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

> The `Action` value above is the authorization-item name for "查询所有备份".
> Confirm the exact literal with the command below — do **not** trust a
> hand-typed action name.

## Verify the action name (mandatory before applying a custom policy)

```text
hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=cbr
```

Copy the exact `name` / `urn_template` values from the response; do not
re-capitalize or normalize them. Alternatively, check the system policy:

```text
hcloud IAM ListPoliciesV5 --cli-region=cn-north-4
hcloud IAM GetPolicyVersionV5 --cli-region=cn-north-4 --policy_id=<policy_id>
```

## 403 troubleshooting

If the script reports `无权限访问 CBR，请检查 IAM 权限`:

1. Confirm the AK/SK belongs to an IAM user in the target account and that the
   hcloud profile uses those credentials.
2. Grant the read-only listing action (system policy above) or the custom
   policy.
3. Re-run `python3 scripts/list_cbr_backups.py`.

> No write/delete actions (create / delete / restore / copy / update) are
> included — this skill never modifies resources.