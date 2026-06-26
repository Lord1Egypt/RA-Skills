# PII & Sensitive Data Redaction Rules

## Purpose

Before any report is generated or shared, all data that will appear in the report must pass through a redaction filter. This protects participant privacy while preserving the research value of the data.

## Always Redact

| Data Type | Replacement | Example |
|-----------|-------------|---------|
| Full names of people | Role-based label | "John Smith" → `[User]`, "Sarah from marketing" → `[Colleague-1]` |
| Email addresses | `[email-redacted]` | "john@company.com" → `[email-redacted]` |
| Phone numbers | `[phone-redacted]` | "+1-555-123-4567" → `[phone-redacted]` |
| Physical addresses | `[address-redacted]` | "123 Main St, SF" → `[address-redacted]` |
| API keys & tokens | `[credential-redacted]` | "sk-ant-api03-..." → `[credential-redacted]` |
| Passwords | `[credential-redacted]` | — |
| Financial account numbers | `[account-redacted]` | Bank accounts, credit cards |
| SSN / government IDs | `[id-redacted]` | — |
| IP addresses | `[ip-redacted]` | "192.168.1.1" → `[ip-redacted]` |
| URLs with auth tokens | `[authenticated-url-redacted]` | URLs containing session IDs, tokens, keys |
| Confidential project names | `[project-redacted]` | Internal codenames (unless user whitelisted) |

## Always Preserve (do NOT redact)

- Use case categories and task descriptions (research data)
- Tool names and skill names (OpenClaw system data, not PII)
- Model names and configuration details
- General emotional language and reactions
- Timestamps and durations
- Error messages and stack traces (redact any embedded PII within them)
- File paths (unless they contain username or PII)

## Detection Heuristics

When scanning text for redaction:

1. **Email pattern:** Look for `word@word.word` patterns
2. **Phone pattern:** Sequences of 7-15 digits, optionally with dashes, spaces, parentheses, or + prefix
3. **Names:** Known names from the conversation, names following "Dear", "Hi", "@", "From:", "To:"
4. **API keys:** Strings starting with common prefixes: `sk-`, `api-`, `token-`, `key-`, `Bearer `, strings that look like base64 and are 20+ characters
5. **Addresses:** Patterns with street numbers + street names + city/state/zip
6. **URLs with auth:** URLs containing `token=`, `key=`, `session=`, `auth=`, `access_token=`
7. **IP addresses:** `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}`

## User Overrides

Users can whitelist specific items via config:

```json
{
  "redaction_overrides": [
    { "type": "project_name", "value": "Project Aurora", "action": "preserve" },
    { "type": "name", "value": "Acme Corp", "action": "preserve" }
  ]
}
```

When the user says "don't redact [X]", add it to `redaction_overrides` in `config.json`.

## Redaction Log

Every redaction is logged to `~/.uxr-observer/redaction-log.json`:

```json
{
  "timestamp": "ISO-8601",
  "report_id": "report-2026-03-03",
  "redactions": [
    {
      "original_category": "email_address",
      "replacement": "[email-redacted]",
      "location": "observation obs-abc123, field user.request_verbatim",
      "reason": "PII auto-redaction policy"
    }
  ],
  "total_redactions": 12,
  "categories_affected": ["email_address", "person_name", "api_key"]
}
```

Note: The log stores the CATEGORY of what was redacted, never the original value.

## Edge Cases

- **User's own name:** Always redact in reports unless user explicitly whitelists
- **Company names:** Redact if they appear to be the user's employer. Preserve if they're public entities being discussed (e.g., "I was reading about Google's API")
- **Code snippets:** Preserve the code structure but redact any hardcoded credentials, connection strings, or PII within the code
- **File paths:** Redact if they contain `/Users/[username]/` or similar identifying paths. Replace username portion with `[user]`
- **URLs:** Preserve domain and path structure, redact query parameters that look like auth tokens
