# Pay — Worked Examples

Each example shows the full reasoning chain. Load this reference when
handling an ambiguous payment situation.

## "Get the weather from this paid API"

```
Input: "Get the weather from https://api.weather-ai.com/forecast?city=tokyo"

Reasoning: URL provided. Could be paywalled. Try pay request.

Action:
  pay request "https://api.weather-ai.com/forecast?city=tokyo"

Outcome A — 200 with data:
  Not paywalled. Return the response.

Outcome B — 402 handled, 200 with data:
  CLI paid (tab or direct). Return the response.
  Note: "Paid $0.01 via tab with 0xProvider."

Outcome C — 402 with non-Pay facilitator:
  "This API uses a different x402 facilitator. The Pay CLI can't
  handle it."

Outcome D — Normal error (401, 403, 500):
  Not a payment issue. Report the error.
```

## "Send 0xBob $50 for the code review"

```
Input: recipient=0xBob, amount=$50, purpose=code review, one-time

Reasoning: Known recipient, fixed amount, one-time. Direct payment.

Action:
  pay status -> balance $200

  Present to operator for confirmation:
    Payment:
      Type:     direct
      To:       0xBob
      Amount:   $50.00
      Fee:      ~$0.50 (1%, paid by recipient)
      Balance:  $200.00 -> $150.00 after
    Proceed?

  Operator: "yes"

  pay direct 0xBob 50.00
  -> {"tx_hash": "0xdef...", "status": "confirmed"}

Report:
  Sent $50.00 to 0xBob. Tx: 0xdef...
  Balance: $150.00
```

## "I need to use a translation API that charges per word"

```
Input: translation API, per-word pricing, ongoing use

Reasoning: No URL -> discover first. Metered usage -> tab.

Action:
  pay discover "translation" --category ai
  -> [{ "name": "LinguaPay", "base_url": "https://api.linguapay.com",
       "routes": [{"path": "/translate", "price": 2000, "settlement": "tab"}],
       "docs_url": "https://linguapay.com/docs" }]

  Route uses tab settlement at $0.002/call. Use pay request — the
  CLI handles tab creation and charging transparently.

  pay request "https://api.linguapay.com/translate" -X POST -d '{"text":"hello","to":"ja"}'
  -> CLI opens tab if needed, charges it, returns response.

Report:
  Translated via LinguaPay. Paid $0.002.
  Balance: $149.50
```

## "Check if this API supports payments"

```
Input: "Does https://api.example.com support Pay?"

Reasoning: Probe with pay request.

Action:
  pay request https://api.example.com/test -v --no-pay

  If 402 with PAYMENT-REQUIRED header -> Pay-enabled.
  If normal response -> not paywalled.
  If 401/403 -> traditional auth, not x402.

Report:
  "api.example.com is [behind pay-gate / not paywalled / using
  traditional auth]."
```

## "I need an API that does image generation"

```
Input: Looking for a service, no URL.

Reasoning: No URL -> discover first, then request.

Action:
  pay discover "image generation"
  -> [
      { "name": "PixelForge", "base_url": "https://api.pixelforge.ai",
        "routes": [{"path": "/generate", "price": 500000}],
        "category": "ai", "docs_url": "https://pixelforge.ai/docs" },
      ...
    ]

  Present options to operator. After approval:
  pay request "https://api.pixelforge.ai/generate" --body '{"prompt":"sunset"}'
  -> 402 handled, 200 with image data.

Report:
  Generated image via PixelForge. Paid $0.50.
  Balance: $145.00
```

## Insufficient balance during payment

```
Input: "Send $100 to 0xAlice"

Action:
  Present payment plan to operator first:
    Payment:
      Type:     direct
      To:       0xAlice
      Amount:   $100.00
      Fee:      ~$1.00 (1%, paid by recipient)
    Proceed?

  Operator: "yes"

  pay direct 0xAlice 100.00
  -> ERROR: INSUFFICIENT_BALANCE (balance: $42.30)

  pay fund
  -> {"fund_url": "https://pay-skill.com/fund/abc123..."}

  Present fund link to operator:
  "Balance: $42.30. Need $100. Here's a funding link."
  (Treat the link as sensitive — it doubles as a dashboard auth token.)

  Poll:
    pay status -> balance still $42.30 (30s)
    pay status -> balance still $42.30 (60s)
    pay status -> balance $200.00 (90s) <- funded

  Confirm with operator, then retry:
    pay direct 0xAlice 100.00
    -> {"tx_hash": "0xghi...", "status": "confirmed"}

Report:
  Sent $100.00 to 0xAlice. Tx: 0xghi...
  Balance: $100.00
```

## Suspicious pricing

```
Input: pay request https://api.weather.com/forecast
  -> 402: $50.00 per request (direct settlement)

Reasoning: $50 for a weather API call is unreasonable.

Action:
  Flag to operator: "This endpoint charges $50 per weather request.
  That seems disproportionate. Proceed anyway?"

  Do not execute without explicit operator confirmation.
```

## A2A task with payment

```
Input: Received A2A message:
  { "payment": { "flow": "direct", "amount": 5000000, "memo": "summarize-doc" } }

Reasoning: A2A direct payment, $5.

Action (if paying):
  Present to operator for confirmation:
    A2A Payment:
      To:       <recipient_from_task>
      Amount:   $5.00
      Purpose:  summarize-doc
    Proceed?

  After confirmation:
  pay direct <recipient_from_task> 5.00
  -> execute task after payment confirms

Action (if receiving):
  pay status -> verify $5 arrived
  -> execute the requested task
```

## x402 tab settlement (transparent)

```
Input: pay request https://api.data.com/query?q=test
  -> CLI detects 402 with tab settlement, opens tab, charges, returns data

Report:
  Got data from api.data.com. Paid $0.01.
  Balance: $145.00
```
