# Postbox Operational Guide

Secondary reference for the Postbox skill. Read sections as needed.

## Authentication Setup

Guide users to set `POSTBOX_API_KEY` as an environment variable. **Never accept API keys pasted in chat.**

Setup instructions to share with user:

1. Go to https://usepostbox.com/integrations/api-keys
2. Create and name a key (shown once)
3. Set as env var:
   - macOS/Linux: `export POSTBOX_API_KEY="..."` in `~/.bashrc` or `~/.zshrc`
   - Windows: `setx POSTBOX_API_KEY "..."`
   - Claude Code: Add to `.env` file
4. Restart session

If user pastes a key in chat, do NOT store or repeat it. Redirect to env var.

## Deployment and Sharing

The endpoint URL opened in a browser shows a documentation page (content negotiation). It is NOT a fillable form. Never suggest it as a way to collect submissions from users.

When user says "deploy" or "share with users," they want their custom HTML/React form hosted:

- **Static hosting**: Netlify, Vercel, GitHub Pages, Cloudflare Pages
- **Embed**: Copy form HTML + script into existing site
- **Framework**: Integrate component into Next.js, Remix, etc.

## Error Handling

All errors: `{"error": {"code": "...", "message": "..."}}`. Validation errors add `details`.

| Status | Code                                    | Action                               |
| ------ | --------------------------------------- | ------------------------------------ |
| 401    | `unauthorized`                          | Re-prompt for API key setup          |
| 403    | `form_limit_reached` / `pro_required`   | Mention upgrade URL                  |
| 404    | `not_found` / `form_not_found`          | Confirm ID/slug                      |
| 422    | `validation_error`                      | Show per-field errors, suggest fixes |
| 429    | `rate_limited` / `plan_limit_exhausted` | Use `retry_after` or mention upgrade |

Present errors in plain language.

## Pricing

- **Free**: 1 form, 5,000 lifetime submissions, 50 AI credits (one-time). AI stops at 0 credits.
- **Pro** ($19/mo or $199/yr): Unlimited forms/submissions, MCP, 500 credits/month, metered overflow.
- Credits: spam $0.005, translation $0.005, smart reply $0.01.
- Standard spam is always free.

Don't push upgrades. Be transparent when Pro is required (MCP, unlimited forms) or credits are involved.

## MCP Setup

Requires Pro plan. Endpoint: `https://usepostbox.com/mcp` (StreamableHTTP, OAuth 2.1).

Claude.ai/ChatGPT: Add remote MCP server in settings with URL above.

CLI config (Claude Code, Cursor):

```json
{
  "mcpServers": {
    "postbox": { "type": "http", "url": "https://usepostbox.com/mcp" }
  }
}
```

## Destinations Quick Reference

CRUD at `/api/forms/{form_id}/destinations`. Types: `webhook`, `discord`, `slack`.

- Webhook: secret (`whsec_...`) shown once at creation. HMAC-SHA256 verification. Regenerate via `/regenerate-secret`.
- Discord/Slack: just provide platform webhook URL. No secret.
- All types: 3 retries, auto-disable after 3 failures.
- Multiple destinations per form allowed.

Proactively suggest for: lead gen (webhook to CRM), support forms (Discord/Slack), any "real-time" or "notifications" mention.
