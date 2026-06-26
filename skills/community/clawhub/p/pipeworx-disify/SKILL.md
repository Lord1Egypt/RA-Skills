---
name: pipeworx-disify
description: Detect disposable and temporary email addresses — validate emails and check domains against known throwaway services
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📧"
    homepage: https://pipeworx.io/packs/disify
---

# Disify — Disposable Email Detection

Is that email real or a throwaway? Disify checks email addresses and domains against a database of known disposable email services like Mailinator, Guerrilla Mail, and Temp Mail. Useful for form validation, anti-fraud, and user quality checks.

## Tools

- **`validate_email`** — Check if an email address is disposable or malformed. Returns format validity and disposable status.
- **`check_domain`** — Check if a domain is associated with disposable email services (e.g., "mailinator.com").

## When to use

- Validating sign-up forms to block throwaway emails
- Screening lead generation forms for quality
- Checking if a domain in your user database is disposable
- Anti-abuse pipelines that need to flag temporary email usage

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/disify/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"validate_email","arguments":{"email":"test@mailinator.com"}}}'
```

```json
{
  "email": "test@mailinator.com",
  "format_valid": true,
  "disposable": true,
  "domain": "mailinator.com"
}
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-disify": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/disify/mcp"]
    }
  }
}
```
