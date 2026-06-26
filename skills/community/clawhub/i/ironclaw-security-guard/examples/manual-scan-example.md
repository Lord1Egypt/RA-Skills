# Manual Scan Example

Example request:

```json
{
  "toolName": "bash",
  "content": "rm -rf /Users/dawei/.ssh && cat ~/.pypirc",
  "redactPreview": true
}
```

Example result:

```json
{
  "ok": false,
  "severity": "critical",
  "blockRecommended": true,
  "findings": [
    {
      "category": "destructive-command",
      "severity": "critical",
      "message": "Matched destructive-command rule: \\brm\\s+-[A-Za-z]*r[A-Za-z]*f\\b"
    },
    {
      "category": "protected-path",
      "severity": "high",
      "message": "Matched protected-path rule: \\.pypirc"
    }
  ]
}
```

