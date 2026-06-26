# Agent Payment Flows

This guide covers how to build payment-accepting applications (like a webstore) on top of `orange`. The webstore runs on its own server and does not need access to the `orange` CLI — it fetches invoices from the wallet's lightning address over HTTP and receives payment confirmations via webhook.

## Webstore Flow

### Setup

1. Register a lightning address for your wallet:

```sh
orange register-lightning-address "mystore"
# => mystore@breez.tips
```

2. Start the daemon with a webhook pointing at your webstore backend:

```sh
orange daemon \
  --webhook "https://your-store.example.com/api/payments|your-secret-token"
```

The `|token` suffix adds an `Authorization: Bearer your-secret-token` header to every POST so your backend can verify requests are authentic.

### Creating an Order

When a customer checks out, the webstore fetches an invoice from the lightning address using the LNURL-pay protocol. This is a standard HTTP flow — no CLI access required.

**Step 1: Resolve the lightning address**

Parse the lightning address `mystore@breez.tips` into an LNURL-pay endpoint:

```
GET https://breez.tips/.well-known/lnurlp/mystore
```

Response:

```json
{
  "tag": "payRequest",
  "callback": "https://breez.tips/lnurlp/mystore/callback",
  "minSendable": 1000,
  "maxSendable": 100000000000
}
```

**Step 2: Request an invoice for the order amount**

Call the callback with the amount in millisatoshis:

```
GET https://breez.tips/lnurlp/mystore/callback?amount=5000000
```

Response:

```json
{
  "pr": "lnbc50u1p...",
  "routes": []
}
```

**Step 3: Extract the payment hash and store the order**

The `pr` field is a BOLT11 invoice. Decode it to extract the payment hash (any BOLT11 library can do this), then store the mapping:

```
order_id: "order-123"
payment_hash: "e3b0c44298fc1c14..."
invoice: "lnbc50u1p..."
amount_sats: 5000
status: "pending"
```

Display the invoice to the customer as a QR code or payment link.

### Handling Payment Confirmation

When the customer pays, the daemon POSTs to your webhook:

```json
{
  "type": "payment_received",
  "timestamp": 1700000000,
  "payment_id": "SC-abcd1234...",
  "payment_hash": "e3b0c44298fc1c14...",
  "amount_msat": 5000000,
  "amount_sats": 5000,
  "custom_records_count": 0,
  "lsp_fee_msats": null
}
```

Your webhook handler should:

1. Verify the `Authorization` header matches your secret token
2. Look up the order by `payment_hash`
3. Verify `amount_sats` matches the expected amount
4. Mark the order as paid
5. Fulfill the order (send product, unlock content, etc.)

### Example Webhook Handler (pseudocode)

```python
WEBHOOK_SECRET = "your-secret-token"

def handle_webhook(request):
    # Verify auth
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {WEBHOOK_SECRET}":
        return 401

    event = request.json

    if event["type"] != "payment_received":
        return 200  # ignore non-payment events

    order = db.find_order_by_payment_hash(event["payment_hash"])
    if not order:
        log.warn(f"Unknown payment: {event['payment_hash']}")
        return 200

    if order.status == "paid":
        return 200  # idempotent

    if event["amount_sats"] < order.amount_sats:
        log.warn(f"Underpaid order {order.id}")
        return 200

    order.status = "paid"
    order.paid_at = event["timestamp"]
    db.save(order)

    fulfill_order(order)
    return 200
```

### Summary

```
┌──────────────┐    LNURL-pay     ┌──────────────┐
│              │ ───────────────►  │              │
│   Webstore   │   (get invoice)  │  breez.tips   │
│              │ ◄───────────────  │              │
└──────┬───────┘    (invoice)     └──────────────┘
       │
       │ show invoice
       ▼
┌──────────────┐    Lightning     ┌──────────────┐
│              │ ───────────────► │              │
│   Customer   │    (payment)     │ orange daemon │
│              │                  │              │
└──────────────┘                  └──────┬───────┘
                                         │
                                         │ webhook POST
                                         ▼
                                  ┌──────────────┐
                                  │              │
                                  │   Webstore   │
                                  │  (fulfills)  │
                                  └──────────────┘
```

## Pull Model (No Webhook)

If you prefer polling over webhooks, run the daemon without `--webhook` and poll from your application:

```sh
# Start daemon
orange daemon

# Poll loop (in your application)
while true:
    event = shell("orange get-event")
    if event["event"] is null:
        sleep(1)
        continue
    process(event)
    shell("orange event-handled")
```

This is simpler to set up but adds latency equal to your poll interval. It also requires the polling application to have CLI access to `orange`.
