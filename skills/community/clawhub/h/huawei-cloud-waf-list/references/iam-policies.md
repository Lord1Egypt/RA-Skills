# IAM Permissions — Least Privilege

This skill is strictly **read-only** and only ever queries WAF protected
websites / domain names. It needs no write permission of any kind.

## Required action

| Service | Action | Resource | Effect |
|---------|--------|----------|--------|
| WAF | `waf:host:list` | `waf:*:*:host/*` | Allow |

## Minimum policy (JSON)

```json
{
  "Version": "1.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "waf:host:list"
      ],
      "Resource": [
        "waf:*:*:host/*"
      ]
    }
  ]
}
```

## Notes

- Without `waf:host:list` the API returns `WAF.00012006` /
  `pdp.permission.denied` and the script prints an explicit permission hint.
- No `waf:host:create` / `waf:host:delete` / `waf:host:update` or any
  policy/rule write action is used or required.
- If the account uses enterprise projects, grant the permission on the target
  project, or query all projects with `--enterprise-project-id all_granted_eps`
  (requires enterprise-project visibility on those projects).