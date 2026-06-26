# ACL template

```json
{
  "groups": {
    "group:admins": ["you@example.com"]
  },
  "hosts": {
    "mac-host": "100.x.y.z"
  },
  "acls": [
    {
      "action": "accept",
      "src": ["group:admins"],
      "dst": ["mac-host:443", "mac-host:22", "mac-host:5900"]
    }
  ]
}
```

Adapt the group, host alias, and IP to the real tailnet. Troubleshooting rule: if both 22 and 5900 are blocked from Windows while the Mac locally shows 5900 listening and local self-test succeeds, inspect Tailscale ACLs first.
