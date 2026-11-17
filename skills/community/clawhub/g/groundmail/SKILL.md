---
name: groundmail
description: >-
  Use when sending or integrating Groundmail transactional email: POST /emails,
  the official SDKs (Node, Python, Go, PHP, Laravel, Symfony Mailer, Ruby), SMTP relay, gm_ API keys, sandbox test
  sends, domain verification, idempotency keys, error codes and hints, webhooks,
  suppressions, templates or the OpenAPI spec. Trigger whenever the user mentions
  Groundmail, groundmail, GROUNDMAIL_API_KEY, gm_ keys, api.groundmail.dev or
  mail.groundmail.dev.
license: MIT
metadata:
  author: groundmail
  homepage: https://docs.groundmail.dev/ai/agent-skills
  source: https://github.com/Groundmail/groundmail-skills
  documentation: https://docs.groundmail.dev/ai/agent-skill
  openclaw:
    homepage: https://docs.groundmail.dev/quickstart
    primaryEnv: GROUNDMAIL_API_KEY
    envVars:
      - name: GROUNDMAIL_API_KEY
        required: false
        description: Groundmail API key (gm_ or gm_test_). Needed to send email or call the API.
---

# Groundmail

Transactional email API on mail servers and IPs Groundmail owns and runs. Send with HTTP, an official SDK (Node, Python, Go, PHP, Ruby), SMTP or MCP.

## Defaults

1. Base URL `https://api.groundmail.dev`, auth `Authorization: Bearer gm_…`, key in env `GROUNDMAIL_API_KEY` (server-side only).
2. Contract: https://docs.groundmail.dev/openapi.yaml · Index: https://docs.groundmail.dev/llms.txt · Full docs: https://docs.groundmail.dev/llms-full.txt
3. Test on the user's own address first (sandbox below). Ask before emailing anyone else, adding a domain or touching billing.
4. Send every email with an `Idempotency-Key` and reuse it on retries.
5. On errors, branch on `error.code` and follow `error.hint`.
6. No account yet: the user signs up free at https://app.groundmail.dev/signup?ref=plugin (test sends to your own address need nothing else; sending to anyone else needs billing set up in the dashboard, not charged on Free). Never create an account for them.
7. Never ask for or accept payment card numbers, passwords, government ID numbers, health information or other sensitive personal data in chat; the user enters billing and account details only in the Groundmail dashboard.

Related skills: `groundmail-mcp`, `groundmail-cli`, `email-best-practices`.

---

## Send: Node.js

```ts
import { Groundmail, GroundmailError } from 'groundmail'

const groundmail = new Groundmail(process.env.GROUNDMAIL_API_KEY!)

try {
  const result = await groundmail.emails.send({
    from: 'hello@yourdomain.com',
    to: 'user@example.com',
    subject: 'Welcome',
    html: '<p>It works.</p>',
    idempotencyKey: `welcome-${user.id}`,
  })
  console.log(result.id, result.status)
} catch (error) {
  if (error instanceof GroundmailError) {
    console.error(error.status, error.code, error.message)
  }
  throw error
}
```

Install: `npm install groundmail`. The SDK **throws** `GroundmailError` (`status`, `code`, `message`, `details`); it does not return `{ data, error }`.

## Send: Go

```bash
go get github.com/Groundmail/groundmail-sdks/go
```

```go
client, err := groundmail.New(os.Getenv("GROUNDMAIL_API_KEY"))
result, err := client.Emails.Send(map[string]any{
	"from": "hello@yourdomain.com", "to": "user@example.com",
	"subject": "Welcome", "html": "<p>It works.</p>",
})
```

Import path: `groundmail "github.com/Groundmail/groundmail-sdks/go"`.

## Send: Python, PHP, Ruby

```bash
pip install groundmail                       # Python (Django backend: pip install 'groundmail[django]')
composer require groundmail/groundmail       # PHP
composer require groundmail/laravel          # Laravel (MAIL_MAILER=groundmail)
composer require groundmail/symfony-mailer   # Symfony Mailer transport
gem install groundmail                       # Ruby (Rails: bundle add groundmail)
```

```python
tx = Groundmail(os.environ["GROUNDMAIL_API_KEY"])  # from groundmail import Groundmail
tx.emails.send(from_="hello@yourdomain.com", to="user@example.com", subject="Welcome", html="<p>It works.</p>")
```

```php
$tx = new \Groundmail\Client(getenv('GROUNDMAIL_API_KEY'));
$tx->emails->send(['from' => 'hello@yourdomain.com', 'to' => 'user@example.com', 'subject' => 'Welcome', 'html' => '<p>It works.</p>']);
```

```ruby
tx = Groundmail::Client.new(ENV.fetch("GROUNDMAIL_API_KEY")) # require "groundmail"
tx.emails.send(from: "hello@yourdomain.com", to: "user@example.com", subject: "Welcome", html: "<p>It works.</p>")
```

Docs: https://docs.groundmail.dev/sdks/python · https://docs.groundmail.dev/sdks/php · https://docs.groundmail.dev/sdks/ruby · https://docs.groundmail.dev/frameworks/laravel · https://docs.groundmail.dev/frameworks/symfony. Any other language: use HTTP or SMTP.

## Send: HTTP

```bash
curl -X POST https://api.groundmail.dev/emails \
  -H "Authorization: Bearer $GROUNDMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: welcome-8812" \
  -d '{"from":"hello@yourdomain.com","to":"user@example.com","subject":"Welcome","html":"<p>It works.</p>"}'
```

Success: `{ "id": "msg_…", "status": "sent" }` (`"scheduled"` with `scheduled_at`).

Canonical fields: `from`, `to`, `cc`, `bcc`, `reply_to`, `subject`, `html`, `text`, `scheduled_at`, `attachments`, `tags`, `headers`, `template`. Migration aliases (`htmlBody`, `replyTo`, …) are accepted, but generate canonical snake_case.

## Send: SMTP

Host `smtp.groundmail.dev`, port `587` (STARTTLS), username `groundmail`, password an SMTP credential (`gmsmtp_…`) from the dashboard or `POST /smtp-credentials`. Same sandbox, domain and billing rules as the API.

---

## Test sends (safe by default)

| Stage | `from` | `to` | Needs |
|-------|--------|------|-------|
| Sandbox | `noreply@mail.groundmail.dev` | The Groundmail account email only | Nothing |
| Own domain, to self | Address on a verified domain | The account email only | Verified domain |
| Production | Address on a verified domain | Anyone | Verified domain + billing set up in the dashboard |

Anything outside these rules returns `403` `forbidden` with a `hint`, and nothing is sent. Test sends are real deliveries to the account owner and count toward quota.

To test without delivering anything: send to a simulator address (`delivered@`, `bounce@`, `block@`, `complaint@`, `suppressed@`, `delayed@simulator.groundmail.dev`; `bounce+tag@…` works) with any key, or use a test key (`gm_test_…`, `POST /api-keys` with `"test": true`). The response and webhooks carry `"test": true`; nothing counts toward quota. Docs: https://docs.groundmail.dev/testing

`POST /emails/test` with `{"event":"email.bounced"}` delivers a simulated webhook event without sending email.

To test signup or password-reset emails end to end (with any email provider): each team has a test domain, `<team>.test.groundmail.dev`; mail to any address there is caught, never delivered. Use a fresh address per test (`groundmail.testInbox.address()`), then `groundmail.testInbox.waitFor({ to })` (or `GET /test-inbox/wait?to=…&timeout=30`, `408 timeout` when nothing arrives) returns the email with `code` and `links` extracted. 100 test emails a month free. Docs: https://docs.groundmail.dev/email-testing

Plans: Free ($0, 3,000/month, 100/day, 3 domains, never charged, billing set up in the dashboard to send to others) · Pay as you go ($15/month with 20,000 emails included, then from $0.70 per 1,000, less as volume grows; sent and received emails count the same; every feature included) · Dedicated ($249/month for your own servers and IPs, on top of pay-as-you-go pricing). Every tier, price and limit as JSON: https://docs.groundmail.dev/pricing.json. Do not recommend a plan change without the user asking.

Docs: https://docs.groundmail.dev/ai/safe-defaults

---

## Idempotency

- Header `Idempotency-Key` on `POST /emails` and `POST /events` (SDK: `idempotencyKey`), up to 256 characters, kept 24 hours per team.
- Same key + same body: the original response is replayed, nothing is sent again.
- Same key + different body, or first request still running: `409 idempotency_conflict`.
- Use one key per logical message (`password-reset-<userId>-<tokenId>`), store it with the job, reuse it on every retry.

---

## Errors

```json
{
  "error": {
    "code": "forbidden",
    "message": "Sandbox sends are limited to owner@example.com. …",
    "hint": "Sandbox sends from noreply@mail.groundmail.dev only go to your own account email. …",
    "docs_url": "https://docs.groundmail.dev/errors#forbidden"
  }
}
```

A few older endpoints return `error` as a string with `code`, `message`, `hint` and `docs_url` beside it: read `typeof body.error === 'object' ? body.error : body`.

| Code | Status | Do this |
|------|--------|---------|
| `validation_error` | 400 / 422 | Fix the field in `message`/`details`. 422 = suppressed or opted-out recipients: do not resend to them |
| `unauthorized` | 401 | Fix the `Authorization: Bearer gm_…` header |
| `forbidden` | 403 | Follow `hint`: verify the domain, keep sandbox sends to the account email, or ask the user to set up billing in the dashboard |
| `insufficient_scope` | 403 | Use a key with the right scope |
| `tenants_not_enabled` | 403 | The request named a tenant on a plan without tenants (pay as you go and Dedicated have them). Remove `tenant` or tell the user |
| `not_found` | 404 | List the collection to find the right id |
| `conflict` | 409 | Reuse the existing resource |
| `idempotency_conflict` | 409 | New key for a new message; wait and retry for in-progress |
| `plan_limit` / `domain_limit` | 429 / 403 | Stop and tell the user (`upgrade_url`) |
| `daily_ramp_limit` | 429 | Daily ramp-up limit (the new account's, or the tenant's when `details.tenant` is set): do not retry now. Send the rest after `details.resets_at` (00:00 UTC); upgrading does not lift it |
| `rate_limited` | 429 | Wait `Retry-After`, retry with the same key |
| `upstream_error` | 502 / 503 | Retry with backoff and the same key |
| `upstream_error` | 504 | May have been sent: check `GET /emails` before anything else |
| `internal_error` / `not_configured` | 500 / 503 | Retry with backoff and the same key |

Full list: https://docs.groundmail.dev/errors

---

## Domain verification

1. `POST /domains` with `{ "name": "yourdomain.com" }`
2. `POST /domains/{id}` with `{ "action": "apply", "provider": "cloudflare" }` (or `godaddy`, `vercel`), or publish the returned `records` by hand
3. `POST /domains/{id}` with `{ "action": "verify" }`. A `400` with `pending: true` means DNS has not propagated: retry in a minute or two, `checks` shows what is missing
4. Switch production `from` to an address on the verified domain

Explain when the user still needs DNS or registrar access.

---

## Templates, webhooks, events

- Send a published template: `template: { id: "<id or alias>", variables: { … } }` instead of `html`/`text`. Starters: `password-reset`, `email-verification`, `welcome`, `invoice`, `team-invite` (`POST /templates/from-starter`).
- React Email: pass `react: <Component />` with `@react-email/render` installed; the SDK renders it to HTML. Guide: https://docs.groundmail.dev/guides/react-email
- Webhooks: `POST /webhooks`; events include delivered, bounced, complained. Verify signatures with the SDK helper.
- `GET /emails`, `GET /emails/{id}` for status; `GET /deliverability` for best-effort metrics (not inbox placement guarantees).
- Sending for your own customers: create a tenant per customer (`POST /tenants` with `external_id`), add their domain with `tenant`, and send with `tenant: "<external_id>"`. Each tenant has its own suppressions, stats, ramp and pause switch; keys and webhook endpoints can be limited to tenants. Pay as you go and Dedicated plans. Guide: https://docs.groundmail.dev/guides/platforms

---

## Anti-patterns

- Putting `gm_` keys in browser, mobile or `NEXT_PUBLIC_`/`VITE_` variables (the API has no CORS on purpose)
- Sending production mail from `noreply@mail.groundmail.dev`
- Retrying sends without an `Idempotency-Key`
- Parsing `message` instead of branching on `code`
- Describing Groundmail as a clone of another provider in customer-facing copy

## MCP and CLI

- MCP: hosted `https://mcp.groundmail.dev/mcp` (OAuth) or `npx -y groundmail-mcp`. See skill `groundmail-mcp` or https://docs.groundmail.dev/ai/mcp
- CLI: skill `groundmail-cli`, `npx -y --package=groundmail-cli -- groundmail …`
