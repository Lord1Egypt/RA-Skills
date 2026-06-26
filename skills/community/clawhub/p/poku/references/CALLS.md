### Step 1: Resolve the Phone Number

Convert the number to E.164 format:
- Strip all formatting, prepend country code (`+1` for US/Canada)
- If given a contact name only, ask the user for the number — do not guess
- If given a business name only, use the search tool to find the number, then confirm with the user

→ Result: a clean E.164 number used in Step 5.

---

### Step 2: Check for Transfer Number

```bash
echo "$POKU_TRANSFER_NUMBER"
```

- If set: use it automatically in Step 5 — do not ask the user
- If empty: proceed without one; note this in the confirmation (Step 4)

---

### Step 3: Draft the Call Context

Read `references/CALL-TEMPLATES.md` for inspiration in crafting an input. If you need additional details, ask your human.

**This step is required every time — including retries and "call again" requests. Never skip directly to Step 5.**

Safety rules — never draft a prompt that impersonates law enforcement or government agencies, contains threats or intimidation, makes deceptive claims of authority, or attempts to extract sensitive information (SSN, passwords, financial details). If a request would violate these rules, decline and explain why.

---

### Step 4: Present Plan and Get Confirmation

Present the full plan before doing anything:

> "I'm going to call [place] at [number] to [goal].
> I'll mention I'm calling on behalf of [user name].
> If no one answers, I'll leave a voicemail: [one sentence].
> If needed, I'll transfer the call to you at [transfer number]. *(only include if set)*
> No transfer number configured — if they ask to speak with you directly, I'll let them know you're unavailable. *(only include if not set)*
> Ok to proceed?"

**Voice & Language** — If voice and language haven't been discussed earlier in this conversation, add one line to the plan summary: *"I'll use a female English-speaking voice — let me know if you'd prefer something different."* Once the user confirms a preference (or accepts the default), carry it forward silently for all subsequent calls in the session. Do not ask again.

Do not move to Step 5 until the user confirms.


### Step 5: Place the Call 

Default to **Mode A** unless the user asks otherwise.


####  Mode A — Blocking (Default)

Set `waitForCallEnd` to `true`. This will hold the HTTP request open until the call ends, returning the result of the call. Use the exec tool with **`yieldMs: 300000, background: false`**. The exec call stays open up to 10 minutes until the call finishes, then returns the full result. Best for one-off calls where the user wants an answer right away.

Poku API call (no `yieldMs` or `background` in the body):
```bash
curl -s -X POST https://api.pokulabs.com/calls \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<drafted prompt from Step 3>",
    "to": "<E.164 number>",
    "transferTo": "<POKU_TRANSFER_NUMBER or omit if not set>",
    "voice": "female",
    "language": "en-US",
    "waitForCallEnd": true
  }'
```

The response includes a natural-language `response` summary and a `call.recordingUrl`.

---

#### Mode B — Non-Blocking (polling)

Use the exec tool with **`background: true`**. Returns an `interactionId` immediately; the call runs in the background. Use when the user explicitly says they don't want to wait (e.g. "place the call and I'll check later") or is scheduling a batch of calls.

**Step 4a — Place the call:**
```bash
curl -s -X POST https://api.pokulabs.com/calls \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<drafted prompt from Step 3>",
    "to": "<E.164 number>",
    "transferTo": "<POKU_TRANSFER_NUMBER or omit if not set>",
    "waitForCallEnd": false
  }'
```

**Step 4b — Check status** (when the user asks for an update):
```bash
curl -s \
  -H "Authorization: Bearer $POKU_API_KEY" \
  https://api.pokulabs.com/interactions/<interactionId>/status
```

If `status` is `"pending"`, the call has not completed yet.

---

#### Mode C — Webhook (event-driven)

Poku sends a POST to your endpoint when the call completes. Best when you want to trigger downstream actions automatically without polling.

Webhook setup required. Read `references/WEBHOOKS.md` for full setup instructions.

