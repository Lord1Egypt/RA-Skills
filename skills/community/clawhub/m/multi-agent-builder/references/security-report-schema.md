# Security Report JSON Schema (for install decisions)

Use this schema for each candidate skill before installation.

```json
{
  "skill": {
    "slug": "string",
    "requested_as": "required|optional",
    "source": "skillhub|clawhub",
    "version": "string",
    "owner": "string"
  },
  "scanner": {
    "name": "skill-vetter|yoder-skill-auditor|manual",
    "status": "ok|fallback|unavailable",
    "timestamp": "ISO-8601"
  },
  "risk": {
    "level": "LOW|MEDIUM|HIGH|EXTREME",
    "signals": [
      "network_access",
      "exec_shell",
      "external_messaging",
      "credential_scope",
      "download_and_execute",
      "obfuscation",
      "privilege_escalation"
    ],
    "notes": "string"
  },
  "decision": {
    "action": "install|block_for_review|skip",
    "reason": "string"
  }
}
```

## Decision policy
- LOW / MEDIUM => `install` (unless explicit org policy denies)
- HIGH / EXTREME => `block_for_review`
- scanner unavailable and no fallback => `skip` + report blocker

## Aggregated summary object
At the end, return a top-level summary:

```json
{
  "summary": {
    "requested": 0,
    "installed": 0,
    "blocked": 0,
    "skipped": 0
  },
  "items": []
}
```
