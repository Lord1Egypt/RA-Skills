# Behavior Rules

## Billing Extraction

Every successful API response must be checked for billing fields in both headers and JSON body.

Header fields:

- `X-Mengguyu-Billing-Charged`
- `X-Mengguyu-Billing-Balance`
- `X-Mengguyu-Billing-Currency`

JSON fields:

- `billingCharged`
- `billingBalance`
- Any returned currency field.

Prefer the header currency. If absent, use a currency literal returned in the JSON body. Do not invent a currency.

Do not use `curl -s` alone when billing matters because it loses headers. Use `curl -sS -i`, `curl -sS -D headers.txt -o body.json`, Python `requests`, or Node `fetch` in a task-local scratch file.

For async endpoints, extract billing from the completed poll response, not only the initial job submission.

## Cost Confirmation

Reference rates from the public Mongol AI skill source. Treat them as estimates unless the API response or provider dashboard says otherwise:

- `/translation`, `/tts`, `/tts/async`: RMB 6 per 10,000 input characters.
- `/chat/completions`: input RMB 60 per million tokens, output RMB 120 per million tokens.

Short text and short chat can be called directly.

Before long text, batches, Word/PDF, OCR, ASR, or TTS, estimate the likely cost and ask the user to confirm.

## Retry and Redo

Do not retry `4xx` responses. Fix API key, required fields, JSON, segmentation, or file limits.

Retry `5xx`, timeout, network reset, or transient transport failures only if no completed success/failure response, no usable `jobId`, and no billing fields were parsed. Use incremental backoff and stop after 3 attempts.

Once a response includes a successful business field or billing fields, treat the request as charged. Do not send the identical payload again unless the user explicitly accepts another charge.

If the user dislikes a translation or output, present the result and billing honestly. For a redo, ask for confirmation and alter the strategy, such as splitting text, changing direction, cleaning OCR noise, or using a different document.

## Billing Disclosure

Parse billing fields after every successful call, but do not display them by default. Treat account balance and exact charge fields as account metadata.

Show billing values only when the user explicitly asks for cost, charge, billing, or balance details. When showing them, use the user's language and locale, and do not force a fixed Chinese line or any other fixed language.

## Final Self-Check

Before final output:

- Confirm every successful call has had headers and body checked for billing.
- Confirm business content uses only the target field for the selected endpoint.
- Confirm billing details are omitted unless the user explicitly requested them.
- If billing details were requested, confirm amounts and currency are copied exactly, without rounding or translation.
- Confirm no raw request payload, raw JSON, token usage, route explanation, or base64 audio is exposed.
