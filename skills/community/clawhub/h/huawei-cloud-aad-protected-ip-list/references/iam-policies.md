# IAM Permissions — Least Privilege

This skill is strictly **read-only** and only ever queries the Anti-DDoS
protected-IP list. It needs no write permission of any kind.

## Required action

| Service | Action | Resource | Effect |
|---------|--------|----------|--------|
| AAD (Anti-DDoS) | `aad:protectedIp:list` | `aad:*:*:protectedIp/*` | Allow |

## Minimum policy (JSON)

```json
{
  "Version": "1.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aad:protectedIp:list"
      ],
      "Resource": [
        "aad:*:*:protectedIp/*"
      ]
    }
  ]
}
```

## Notes

- Without the read-only action the API returns 403 / `not authorized` and the
  script prints an explicit permission hint instead of a traceback.
- No `aad:*:create` / `aad:*:delete` / `aad:*:update` / `associate` /
  `disassociate` / `executeUnblock` action is used or required.
- Action names can differ slightly between IAM policy versions. If
  `aad:protectedIp:list` is rejected when creating the policy, open the IAM
  console → 权限 → AAD and pick the read-only equivalent listed there. Query
  permission is the only capability this skill relies on.
- If the account uses enterprise projects, grant the permission on the target
  project as well.
- The SDK fallback uses the same read-only permission; no additional IAM
  action is needed.