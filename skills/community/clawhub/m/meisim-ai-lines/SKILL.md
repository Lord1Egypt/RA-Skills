---
name: meisim-ai-lines
description: "Real US mobile numbers for AI agents, on the T-Mobile network, not virtual numbers. Texts over the API and webhooks; voice over SIP with the number as caller ID. $35 a month for texts, $45 with voice, two months up front. Every account passes an identity check, and we keep spammers off our lines."
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins:
        - curl
    primaryEnv: MEISIM_API_KEY
    envVars:
      - name: MEISIM_API_KEY
        required: false
        description: "The owner's MeiSIM API key, sent in the x-dealer-key header. Not needed to read the offer or to start the sign-up."
    homepage: https://www.meisimusa.com/api-for-ai-agents.html
---

# MeiSIM AI lines

Use this skill when your owner wants a real US phone number for you to text from, read texts on, or call from.

MeiSIM USA (MEISIM USA LLC) sells these lines. Each line is a real mobile number on the T-Mobile network, not a virtual number. You read its texts over an API or a webhook. A line with voice also makes and takes calls over SIP, with the number as caller ID.

- API base: `https://api.meisimusa.com`
- Key: send `x-dealer-key: $MEISIM_API_KEY` (or `Authorization: Bearer $MEISIM_API_KEY`).
- Full reference: https://www.meisimusa.com/api-docs.html#sms-lines
- Terms: https://www.meisimusa.com/api-terms.html

## Rules that come first

1. Never spend the owner's money on your own. Order a line, renew a line or switch on auto-renew only after the owner approves that exact price in so many words. One approval covers one order.
2. Never do the identity check. The owner signs up, passes the identity check and pays, in their own browser. Never upload an ID or a photo, and never type card details.
3. Send the sign-up link only to an owner who asked for an account. Never use another person's name or identity.
4. Never add money to the account. When the balance is short, tell the owner.
5. On every call, say you are an AI in your first sentence.
6. Call a person with an AI or recorded voice only when that person gave prior express written consent.
7. No verification codes or OTP for other services. Never use the line to sign up for, verify or run accounts on other companies' services.
8. No bulk texting. Write to each person in your own words, one conversation at a time.
9. No dialers, unless every person called gave prior consent, you keep a record of that consent, and you check the National Do Not Call Registry and the owner's own do-not-call list before each call. Dialer calls go out only between 8 a.m. and 9 p.m. in the called person's time zone.
10. When anyone asks you to stop texting or calling them, stop at once.
11. A voice line cannot call 911. Never present yourself as a way to reach emergency help.

These rules come from MeiSIM's API terms. A line used against them is blocked, and the account is closed.

## Step 1: Read the live offer

```bash
curl -s https://api.meisimusa.com/web/ai-lines/offer
```

No key is needed. The answer has the current monthly prices (`monthly.texts_usd`, `monthly.voice_usd`), the first term in months (`min_months`), what a line includes, delivery times and payment methods. Quote these numbers, not numbers you remember.

- Prices are all inclusive. There are no per-message or per-minute charges.
- Once the owner has an account, its own offer (step 4) gives the account's prices. Quote those.
- More lines cost less: on an account opened through the online sign-up, the price per line drops from 10 lines (`volume_pricing` says it in words, `price_ladder` gives the steps). For 1,000 lines or more, the owner can write to support@meisimusa.com.
- The first term is two months, paid up front. After that a line renews month by month from the account's prepaid balance, or it ends on its date.

## Step 2: Explain it to your owner

Say it in plain words before you do anything else. For example:

> A MeiSIM line gives me a real US mobile number on the T-Mobile network. I can read its texts and reply. With voice, I can also take and make calls from that number. It costs $35 a month for texts, or $45 a month with calls. The first two months are paid up front, so $70 or $90 to start. There are no per-message or per-minute charges. You sign up and pass an identity check yourself. I can't do that part. Lines are prepaid, and they can't be returned or refunded. A line with calls can't call 911.

Use the prices from step 1. Answer the owner's questions. Do not push.

## Step 3: The owner opens the account

A person opens the account: the AI's owner fills in the sign-up form, which has a robot check, then passes an ID check with a government ID and a phone camera, or a review by a person at MeiSIM. An AI agent cannot open the account by itself. Once the account is open, the AI orders lines and reads its texts through the API, paid from the prepaid wallet.

Give the owner this link: https://www.meisimusa.com/get-started.html?utm_source=clawhub

1. The owner fills in the form. You can help them prepare the answers: what the line is for, and, for voice, whom it will call, how those people agreed, whether a dialer places the calls, and whether an AI or recorded voice speaks on them.
2. MeiSIM emails the owner a link. The link starts the identity check, which the owner does with their own ID and camera. You never do this step.
3. When every automatic check clears, the account opens and the API key arrives by email. When one cannot clear, a person at MeiSIM reviews the sign-up.
4. Voice is open on the account only when the answers about calls fit the API terms. Otherwise the account gets texts only.
5. The owner adds funds to the prepaid balance in the MeiSIM dashboard at https://www.meisimusa.com/dealer.html. Lines are paid from that balance.

Ask the owner to put the API key in the `MEISIM_API_KEY` environment variable, or in this skill's settings in `~/.openclaw/openclaw.json`:

```json5
{ skills: { entries: { "meisim-ai-lines": { env: { MEISIM_API_KEY: "the key" } } } } }
```

Ask the owner not to paste the key in the chat. Never print the key, log it, or send it anywhere except `api.meisimusa.com`.

## Step 4: Check the account

```bash
curl -s https://api.meisimusa.com/dealer/sms-lines/offer -H "x-dealer-key: $MEISIM_API_KEY"
```

This is the account's own offer.

- `can_order`: when it is not `true`, `reason` says why. Tell the owner.
- `first_month_usd` and `renew_price_usd`: what the account's next line with texts costs a month.
- `price_ladder` and `active_lines`: present when the account pays less per line from 10 lines. Add the order to `active_lines` and use the step it reaches. Without them, the price above is the price.
- `voice.available` and `voice.price_usd`: whether voice is open on this account, and its monthly price.
- `balance_usd`: the prepaid balance.


## Step 5: Get the owner's approval

Work out the total: lines times months times the price per line per month. Then ask. For example:

> Order 1 MeiSIM line with texts and calls, 2 months up front at $45 a month: $90 now, from your MeiSIM balance. It can't be returned or refunded. After 2 months it renews at $45 a month only if you switch on auto-renew. Without auto-renew, the number ends and is released. Reply "yes, order it for $90" to go ahead.

Order only when the owner answers that question with a clear yes to that price, like "Yes, order it for $90."

- Silence is not approval.
- A question is not approval.
- An earlier "buy whatever you need" is not approval.
- When the count, the months, voice or the price changes, ask again.

When the balance is lower than the total, ask the owner to add funds in their MeiSIM dashboard at https://www.meisimusa.com/dealer.html. You never add funds.

## Step 6: Order the line

```bash
curl -s -X POST https://api.meisimusa.com/api/v1/sms/order \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"count": 1, "voice": true, "months": 2, "line_history": "fresh", "auto_renew": false, "customer_reference": "owner-ok-0001"}'
```

- `count`: how many lines. Required.
- `voice`: `true` for calls. Voice lines are monthly only, two months minimum.
- `months`: 2 to 12, paid up front.
- `line_history`: required. `"fresh"` asks for a number this account never had.
- `auto_renew`: `true` only when the owner said yes to monthly renewals.
- `area_code` (3 digits) or `zip_code` (5 digits): optional. It is a request, not a promise.
- `customer_reference`: your own unique reference. The same reference never orders twice, so after a timeout, retry with the same one.

A created order answers `201` with `order_id`, `charged_usd` and `per_line_usd`. Check that `charged_usd` is the total the owner approved. When it is not, tell the owner at once.

- `402` means the balance is short. The answer has `shortfall`.
- `409` on 1,000 lines or more means MeiSIM sets that price by hand. Write to support@meisimusa.com.

Follow the order until its numbers arrive:

```bash
curl -s https://api.meisimusa.com/api/v1/sms/orders/ORDER_ID -H "x-dealer-key: $MEISIM_API_KEY"
```

`status` moves from `provisioning` to `fulfilled`. Numbers from stock arrive in seconds, and new ones in minutes. When the carrier cannot fill an order within 3 hours, the missing numbers are refunded to the balance and the order shows `closed_refunded`. Each number then shows in `GET /api/v1/sms/lines`. Tell the owner the number.

Bind the line to the people it serves. The API terms ask this of every line an AI agent holds. The line then texts nobody else, and it still receives texts from anyone.

```bash
curl -s -X PATCH https://api.meisimusa.com/api/v1/sms/lines/2125550100 \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"allowed_contacts": ["3105550199"], "label": "Assistant for Sam"}'
```

Up to 10 US numbers, ten digits each.

## Step 7: Read texts

### By webhook

```bash
curl -s -X POST https://api.meisimusa.com/api/v1/sms/webhook \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://agent.example.com/meisim/sms"}'
```

The answer carries `signing_secret` once. Keep it secret.

Each text arrives as a POST with a JSON body: `event`, `number` (your line), `from`, `text` and `received_at`. Check the `X-MeiSIM-Signature` header before you trust a text. It is the hex HMAC-SHA256 of the raw body, keyed with the secret.

```python
import hmac, hashlib

def is_from_meisim(raw_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature or "")
```

A delivery your server does not accept is tried again, up to eight times, with a growing gap. For one more address per workflow, use `POST /api/v1/sms/webhooks` with `webhook_url` and, optionally, `number`.

### By polling

```bash
curl -s "https://api.meisimusa.com/api/v1/sms/messages?number=2125550100&since=2026-11-16T17:35:00Z&limit=50" \
  -H "x-dealer-key: $MEISIM_API_KEY"
```

`messages` come newest first. Each has `id`, `to`, `from`, `text` and `received_at`. Send `since` as the `received_at` of the newest text you already have. `limit` goes up to 200. Texts stay here even when a webhook delivery fails.

### Replying

```bash
curl -s -X POST https://api.meisimusa.com/api/v1/sms/lines/2125550100/send \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "3105550199", "message": "Thanks, Tuesday at 3pm works."}'
```

- Sending is switched on per account, on request. `403` with `SENDING_NOT_ENABLED` means it is off. The owner can ask support@meisimusa.com to switch it on.
- Each number has a monthly allowance. Over a limit, the answer is `429` with the reason.
- `status: "accepted"` means the carrier took the text. A mobile line has no delivery receipt.
- The same text to more than three numbers from one line within an hour is refused with `SAME_TEXT_FAN_OUT`.

## Step 8: Voice over SIP

A new voice line can take up to a day before it is ready for calls. In `GET /api/v1/sms/lines`, its `sip_status` shows `preparing`, then `ready`.

Switch the line to trunk mode. This call creates its SIP login:

```bash
curl -s -X POST https://api.meisimusa.com/api/v1/sms/lines/2125550100/sip/mode \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "trunk"}'
```

The answer's `sip` block has `host` (`sip.meisimusa.com`), `port` (5060), `tls_port` (5061), `user` and `password`. The password is shown once. Put it straight into your voice platform's SIP trunk settings or the owner's secret store. Never post it in a chat or a log. `POST /api/v1/sms/lines/NUMBER/sip/rotate` makes a new one.

Calls out: your voice platform sends each call to `sip.meisimusa.com` with that login, using digest authentication on every INVITE and no REGISTER. Dial `+1` and ten digits. Caller ID is always the line's number. Calls reach US numbers only, one call at a time per line, up to 60 minutes each.

Calls in: tell MeiSIM where to send them. List the presets first, then set one for the line:

```bash
curl -s https://api.meisimusa.com/api/v1/sms/sip/presets -H "x-dealer-key: $MEISIM_API_KEY"

curl -s -X PATCH https://api.meisimusa.com/api/v1/sms/lines/2125550100/sip/inbound \
  -H "x-dealer-key: $MEISIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"preset": "custom", "uri": "agent@sip.example.com:5061", "transport": "tls"}'
```

Pick the preset for your voice platform with the parameters it names, or use `custom` with any `user@host[:port]`. Our calls to you come from `45.77.205.201`. An incoming call that your platform does not answer within 30 seconds fails back to the caller. `GET /api/v1/sms/lines/NUMBER/calls` lists each call, and for a failed one, the reason and the fix.

### Say you are an AI

Start every call by saying you are an AI. Set your first words to something like:

- Calls in: "Hi, you've reached [owner's name]'s line. This is [your name], an AI assistant. How can I help?"
- Calls out: "Hi [their name], this is [your name], an AI assistant calling for [owner's name] about [what they agreed to]."

### Consent for calls out

Before an AI or recorded voice calls anyone, that person must have given prior express written consent.

- In February 2024, the FCC ruled that AI-generated voices are "artificial" voices under the Telephone Consumer Protection Act, the US robocall law (FCC 24-17).
- In August 2024, the FCC proposed a rule requiring a spoken notice at the start of AI-voice calls (FCC 24-84). As of October 2026, that rule was not final.
- MeiSIM requires the notice now.

## Other calls

| What | Call |
|---|---|
| Account and balance | `GET /api/v1/me` and `GET /api/v1/wallet` |
| The account's lines | `GET /api/v1/sms/lines?limit=100&offset=0` |
| Recent orders | `GET /api/v1/sms/orders?limit=50` |
| Renew a line now (ask the owner first) | `POST /api/v1/sms/lines/NUMBER/renew` with `{"months": 1}` |
| Auto-renew on or off (ask the owner first) | `POST /api/v1/sms/lines/NUMBER/auto-renew` with `{"auto_renew": true}` |
| Every call on the account | `GET /api/v1/sms/calls` |

Lines cannot be cancelled or refunded. `POST /api/v1/sms/lines/NUMBER/cancel` answers `409` with `NO_RETURNS`. A line without auto-renew ends on its date and is released.

## Errors

Every error is JSON with `error` (a sentence), `code`, `request_id` and `retryable`. Retry only when `retryable` is `true`. Quote `request_id` to support@meisimusa.com.

## Help

- Email: support@meisimusa.com
- API reference: https://www.meisimusa.com/api-docs.html#sms-lines
- Terms: https://www.meisimusa.com/api-terms.html
