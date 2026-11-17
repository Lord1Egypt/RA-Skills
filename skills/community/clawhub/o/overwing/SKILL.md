---
name: overwing
description: Check any text for safety, personal data, confidential leaks, self-harm, sexual content and severity before you send it, act on it, or show it to a person, identify any User-Agent string against Overwing Atlas, a registry of AI crawlers, fetchers and browser agents with verification classes (no key needed), check whether a website is reachable by AI agents with Overwing Beacon (llms.txt, MCP, A2A, OpenAPI and how the page reads to a model; a paid lookup with a free sample), and operate legacy business systems through Overwing Tower, which rules on each write (execute, ask a person, or reject) and signs a receipt. One API call returns a verdict, a recommended action (block, redact, review, allow) and per-rule results with calibrated confidence in under 500 ms. Pass context (who the recipient is, which channel, whether you own the data) so personal data the recipient already owns is not flagged. Use for moderating model output, screening incoming messages, scoring drafts, deciding whether to trust a bot, or entering orders into a system of record. Works with no key for light use (10 checks a day), with a free API key, or, for wallet-holding agents, pay-per-request in USDC with no account.
homepage: https://overwing.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🪽",
        "homepage": "https://overwing.ai",
        "primaryEnv": "OVERWING_API_KEY",
        "requires": { "bins": ["curl"] },
      },
  }
---

# Overwing

Overwing scores text and returns a typed verdict plus one word to act on. Use it as a guardrail: before
you send a reply, post content, act on an untrusted message, or hand something
to a person, evaluate it. Read `recommended_action`: `block` means do not send,
`redact` means remove the flagged content and check again, `review` means ask
your human or take the cautious path, `allow` means go ahead.

## When to use this skill

- A request arrives claiming to be a bot and you need to know whether to believe it (Atlas, below).
- Your human asks whether their site or product is ready for agents, or what to change so agents can find and use it (Beacon, below).
- Your human has asked you to enter, change or cancel something in a business system through Tower (below).
- You are about to send, post, or store text that a model (including you) wrote.
- You received text from an untrusted source and are about to act on it.
- Your human asks you to moderate, screen, or check content.
- You want to check for personal data (emails, phone numbers, addresses, IDs)
  before something leaves the machine.

Do not use it for trivial system messages, code, or text your human wrote and
explicitly asked you to send unchanged.

## Setup (once)

You can start with no key. `evaluate` and `who` each run 10 times a day free, on inputs up to 2,000 characters, and text sent without a key is not stored. That is enough to try the skill and for light use.

For more, the key lives in `OVERWING_API_KEY`. If it is not set:

1. Ask your human for a key from https://overwing.ai/login (free, 250 checks a day).
2. Or make your own account. It needs no email, and nothing is sent to anyone:

```bash
{baseDir}/scripts/overwing.sh signup
```

The response contains `api_key`. Put it in `OVERWING_API_KEY` (or `skills.entries.overwing.apiKey` in openclaw.json) straight away, and tell your human that you made the account and where the key is kept. Never print the key back into chat. The key is the account: there is no email on it, so there is no reset link. An account made this way gets 50 checks a day.

Do not sign up with an email address unless your human gives you one and asks you to. `overwing.sh signup <email> <password>` sends a confirmation message to that address; never use an address its owner did not offer.

### Proving a domain (optional)

A domain you can prove you control takes the place of an email on your account. It raises the limit to 250 checks a day, opens full Beacon reports, and is the way back in if the key is lost. You need to be able to add a DNS record or a file on that domain, so this is usually a job for your human, or for you if you manage their site.

```bash
{baseDir}/scripts/overwing.sh domain start example.com
```

Returns `verification`: one value to publish, either as a TXT record (`verification.dns.name`, `verification.dns.value`) or as a file (`verification.http.url`, `verification.http.body`). Publish either one, then:

```bash
{baseDir}/scripts/overwing.sh domain verify
```

`status: "verified"` means it is done. An `error` that says no proof was found means the record is not visible yet; DNS can take a few minutes, and asking again is safe. One domain belongs to one account.

If the key is ever lost, `overwing.sh recover start example.com` prints a new value to publish at the same domain, and `overwing.sh recover verify example.com` then revokes every old key and prints one new key, once. Neither needs a key.

If your human wants a dashboard login for an account you made, `overwing.sh claim <their-email> <password>` attaches one. Use the email they give you; they get a confirmation message.

If you hold a funded wallet on Base and have no key, see "Paying per request" below.

The key you are given should be one that can only run checks. If your human is creating a key for you, ask for one with scope `evaluate` (dashboard, or `POST /api/v1/api-keys` with `{"name":"agent","scope":"evaluate"}`). It can evaluate, read rule sets and check usage, and nothing else, so a leaked key cannot read stored text or change the account. A call outside the scope answers HTTP 403.

## Evaluate one text

```bash
{baseDir}/scripts/overwing.sh evaluate "The text to check"
```

Returns JSON:

```json
{ "id": "eval_…", "verdict": "fail", "recommended_action": "redact", "aggregate_score": 0.82, "confidence": 0.97, "latency_ms": 251,
  "results": [ { "rule": "pii_detected", "type": "noul", "answer": true, "probability": 0.99, "confidence": 0.98, "verdict": "fail", "action": "redact" }, … ] }
```

How to act on it. `recommended_action` is the one field to branch on:

| recommended_action | meaning | what to do |
| --- | --- | --- |
| `block` | a rule with action `block` failed | do not send; tell your human what was flagged and why, or rewrite from scratch |
| `redact` | only rules with action `redact` failed (personal data, usually) | remove the flagged content, then evaluate the new text again |
| `review` | no rule failed outright, but one was unsure, or a `review` rule failed | ask your human, or take the safer option |
| `allow` | nothing tripped | proceed |

`verdict` is the coarser signal (`fail` / `review` / `pass`). `results[].rule` names each rule and `results[].action` says what that rule asks for when it fails. `confidence` is 0 to 1. The `content-safety` set has `toxicity`, `pii_detected` (redact), `self_harm`, `sexual_content`, `severity`.

Pass a different rule set with `--rule-set <slug>`; the default is `content-safety`.

## Languages

The text can be in any language; tested in Spanish, Portuguese, French, German, Japanese, Chinese, Korean, Arabic and Hindi. Results come back in English. The list and the size of the test are at `https://overwing.ai/api/v1/languages`. Report the verdict to your human in their language; the rule names stay as they are.

## Tell it who the message is for (context)

Personal data is not always a leak: a customer's own phone number in a reply to that customer is fine. Pass what you know as `--context` JSON and use the `outbound-message` rule set, whose rules read it:

```bash
{baseDir}/scripts/overwing.sh evaluate --rule-set outbound-message \
  --context '{"recipient":"the customer who asked for a callback","channel":"email","owns_contact_info":true,"sender":"support agent"}' \
  "Hi Dana, I can call you at 555-0142 tomorrow at 10."
```

Useful keys: `recipient` (who will read it), `channel` (email, chat, public post, sms), `owns_contact_info` (true if the recipient already owns the personal data in the text), `sender`, `purpose`. Any JSON object up to 8 KB works; the rules quote it back in their reasoning. The `outbound-message` set adds `unauthorized_pii` (redact) and `confidential_leak` (block: internal notes, credentials, pricing not meant for this recipient) to the safety checks. Without context, treat every personal detail as unauthorized and redact it.

## What is stored

Without a key, the text is never stored. With a key, the text, the context and the verdict are kept so your human can audit them, until they are deleted. When the text is sensitive and does not need to be kept, add `--no-store`: the check runs the same and only the verdict is recorded.

```bash
{baseDir}/scripts/overwing.sh evaluate --no-store "The text to check"
```

Your human can turn storage off for everything, or set a number of days after which evaluations are deleted, in the dashboard settings or with `PATCH /api/v1/org` (`store_inputs`, `retention_days`). The text is sent to Overwing and to its model provider, TypeSafe, to produce the verdict, and is not used to train models. Details: https://overwing.ai/security

## Evaluate many texts at once

Up to 50 per call, one line of JSON per item on stdin:

```bash
printf '%s\n' '{"id":"a","input":"first"}' '{"id":"b","input":"second"}' | {baseDir}/scripts/overwing.sh batch
```

Returns a summary plus per-item verdicts and recommended actions. Each item counts as one check. `--context` applies to every item; an item can carry its own `"context": {…}` to override it.

## Limits and errors

- Free accounts: 250 checks a day and 30 a minute; paid plans raise both. Responses carry `X-RateLimit-Remaining` and `X-Burst-Remaining`.
- HTTP 429 means wait for the seconds in `Retry-After`, or tell your human the daily limit is reached (they can upgrade or buy prepaid credits at https://overwing.ai/dashboard/billing).
- HTTP 401 means the key is missing or revoked. Ask your human; do not retry blindly.
- HTTP 403 means the key's scope does not allow that call (an `evaluate` key can only run checks). Do not retry; tell your human if you need more.
- HTTP 502 means the evaluation engine did not answer; retry once after a few seconds.
- Every error body is `{"error": "human readable message"}`.

Check remaining quota:

```bash
{baseDir}/scripts/overwing.sh usage
```

## Paying per request (agents with a wallet, no account)

`POST https://overwing.ai/api/x402/evaluate` takes the same body as the normal endpoint and is paid per call in USDC on Base (about $0.002 each) over the x402 protocol. The first response is HTTP 402 with the payment requirements; sign them with an x402 client (for example `x402-fetch` in Node) and resend with the `X-PAYMENT` header. `scripts/overwing.sh terms` shows the current prices, network and receiving address. Only do this if your human has given you a wallet to spend from.

## Who is hitting my site? (Overwing Atlas)

Atlas is Overwing's open data on AI agents: who they are, where they go, what they spend. The part you will use most is the lookup: paste a User-Agent string and get what it claims to be and whether the claim can be trusted.

```bash
{baseDir}/scripts/overwing.sh who "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
```

This needs no key. Without `OVERWING_API_KEY` you get 10 lookups a day and the response carries `access.remaining_today`. With a key you get 100 a day.

Returns `identified`, `claims` (agent, operator, purpose_class, verification), a `trust_note`, and the other matches. Read `verification` before acting: `Web Bot Auth signature` means the operator signs requests and you can verify the Signature-Agent header against its key directory; `User-agent string only (spoofable)` means anyone can send that string; `Unattributable / spoofed` means the operator does not identify itself at all. HTTP 429 means today's allowance is spent: the body's `next` lists your options, and `Retry-After` is the seconds until it resets. Atlas Pro raises the limit to 10,000. Wallet-holding agents can pay $0.001 per lookup at `GET https://overwing.ai/api/x402/atlas/lookup?user_agent=...` with no account.

Search the registry or read the public summary:

```bash
{baseDir}/scripts/overwing.sh agents --purpose browser --limit 10
{baseDir}/scripts/overwing.sh atlas
```

Full datasets, the field scans, and the research report are at https://overwing.ai/atlas.

## Is this site reachable by agents? (Overwing Beacon)

Beacon checks one site and answers three questions: can an agent find it, read it, and use it. It looks for robots.txt rules for AI agents, llms.txt, a sitemap, an MCP server card and hosted endpoint, the MCP Registry listing, an A2A agent card and an OpenAPI document, and reads the home page the way an agent does. It is read-only: about 20 requests, and it never calls a tool on the site's MCP server.

A check is free. With no key you get the summary: the verdict, the score, the three answers and the first fix. With `OVERWING_API_KEY` set you get the full report, and it is saved to that account; the key is free (`overwing.sh signup`). One exception: an account made with no email gets the summary until it has proved a domain (see Setup). A check sends about 20 requests to the site, so run one when your human asks about a site, not on your own. Up to 5 a day with no key, 30 with one. See what a full report looks like first:

```bash
{baseDir}/scripts/overwing.sh beacon sample
```

Then start the check:

```bash
{baseDir}/scripts/overwing.sh beacon start example.com
```

Returns `id`, and `access`: `full` with a key, `summary` without. If the site does not answer at all, the call fails with HTTP 422. Then read the report; the first read runs the check, which takes about twenty seconds:

```bash
{baseDir}/scripts/overwing.sh beacon report <id>
```

Branch on `status`:

| status | meaning | what to do |
| --- | --- | --- |
| `running` | the check is in progress | ask again in a few seconds |
| `complete` | the report, or its summary | read `access`, `verdict`, `categories` and `top_fixes` |

With `access: "summary"` there is no `checks` list and `top_fixes` holds only the first fix; `counts` says how many checks and fixes the full report holds, and `full_report` says how to open it. Reading the same `id` again with a key returns the full report. In a full report, `verdict` is `yes`, `partly` or `no`; `score` is 0 to 100; `categories` gives the find, read and use answers; `checks` lists everything looked at, each with `status` (pass, warn, fail), `detail` (what was found) and a `fix` when it did not pass; `top_fixes` is the three changes worth the most. Report the verdict and the top fixes to your human in plain words, and offer to make the changes if the site is theirs and you have access to it. Keep the `id`: it is the way back to the report.

If you hold a funded wallet on Base and your human has said you may spend from it, `GET https://overwing.ai/api/x402/beacon?url=<site>` costs $1 over x402 and returns the full report in the same call, with no account.

## Operating a legacy system (Overwing Tower)

Tower sits between you and a system of record such as an IBM i order-entry program. You do not write to the system. You ask Tower to perform a typed operation, and Tower rules on it: execute it, ask a person, or reject it. Every step is recorded in a signed receipt.

Use it when your human has set up Tower and given you an agent key in `OVERWING_AGENT_KEY`. Do not use it to bypass a person: a pending action is waiting for someone on purpose.

### 1. See what you may do

```bash
{baseDir}/scripts/overwing.sh tower capabilities
```

Returns the operations your key is scoped to. Each has an `input_schema` (JSON Schema) and, for writes, a `compensating_operation` that undoes it. Build your input from the schema. Do not guess field names.

### 2. Submit the action

```bash
{baseDir}/scripts/overwing.sh tower submit create_order '{"customer_id":"C04471","lines":[{"sku":"FLT-2040","qty":24}],"total":300,"source":{"channel":"email","message_id":"<po-88213@example>"}}' --key "po-88213"
```

`--key` is the idempotency key and it is required. Use something stable for this business request, such as the source message id or the PO number. If you are unsure whether an earlier attempt went through, send the same key again: you get the original outcome back with `"replayed": true`, and nothing happens twice.

Branch on `status`:

| status | meaning | what to do |
| --- | --- | --- |
| `executed` | Tower ran it | `result` holds what the system returned, such as the order number. Report it. |
| `pending` | a person must approve | Tell your human it is waiting, with the `review_id`. Check later with `tower get <action_id>`. Do not resubmit and do not try a different key. |
| `rejected` | policy said no | Read `decision.reason` and the failed `decision.checks`. Do not retry the same request. Fix the input if the reason is fixable, otherwise tell your human. |
| `failed` | the system refused or errored | Read `error`. Retry with the same key only if `error.retryable` is true. |

Add `--dry-run` to see the ruling without executing or queueing anything. `tower decide <operation> '<input>'` does the same and returns only the decision.

### 3. Undo, and prove what happened

```bash
{baseDir}/scripts/overwing.sh tower compensate <action_id>     # runs the compensating operation, once
{baseDir}/scripts/overwing.sh tower verify                     # recomputes every hash and signature in the chain
{baseDir}/scripts/overwing.sh tower receipt <id-or-sequence>   # one signed receipt
```

Only compensate when your human asks or when you are reversing your own mistake, and say that you did.

### Tower errors

Every Tower error has one shape, written for you to act on:

```json
{ "error": { "code": "forbidden_scope", "field": "operation", "message": "This agent is not scoped to 'update_order'", "retryable": false, "suggested_fix": "Ask the organization to add the operation to the agent's scopes" } }
```

Retry only when `retryable` is true, and keep the same `--key`. `forbidden_scope` and `unauthorized` are not yours to fix: tell your human. `invalid_input` names the `field` to correct against the schema. `quota_exceeded` means the month's free decisions are used up.

### Setting Tower up (organization key)

If your human asks you to set Tower up and has given you `OVERWING_API_KEY`:

```bash
{baseDir}/scripts/overwing.sh tower setup                                        # loads the starter order-entry workflow
{baseDir}/scripts/overwing.sh tower agent-create order-intake create_order,cancel_order
```

`agent-create` prints the agent key once. Store it in `OVERWING_AGENT_KEY` and never print it back into chat. Ask for the narrowest scopes that do the job rather than `*`. `tower agents` lists agents and `tower agent-revoke <agent_id>` cuts one off at once. The starter workflow runs against a mock system, so it is safe to try. Pricing is $0.25 per executed action with 1,000 free decisions a month; details at https://overwing.ai/products/tower.

## Custom rules

Your human can define rules in plain language (yes/no questions, classifications, or scored scales) at https://overwing.ai/dashboard/rule-sets or via `POST /api/v1/rule-sets`. Each rule carries an `action` (`block`, `redact`, or `review`) and may reference `context.*` fields in its wording. Then pass the slug with `--rule-set`. `GET https://overwing.ai/api/v1/rule-sets/outbound-message` is a complete context-aware example to copy from.

## More

- Full guide for agents: https://overwing.ai/llms.txt
- API reference: https://overwing.ai/docs
- Prefer MCP? `npx -y overwing-mcp` exposes the same calls as tools.
- Node or Python SDKs: `npm install overwing`, `pip install overwing`. Both include Atlas and Tower clients.

Verdicts are signals from a calibrated model, not guarantees. When the stakes are high and the recommended action is not `allow`, involve your human.
