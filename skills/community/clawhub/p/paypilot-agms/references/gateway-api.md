# Gateway API Reference

## Overview
PayPilot uses a secure payment gateway proxy. All gateway interactions go through the PayPilot API — you never call the underlying gateway directly.

## Authentication & Onboarding

### Register
```
POST /v1/auth/register
{
  "name": "Business Name",
  "email": "merchant@example.com",
  "password": "strong_password"
}
```

### Login
Returns a JWT access token.
```
POST /v1/auth/login
{
  "email": "merchant@example.com",
  "password": "strong_password"
}
```

### Configure Gateway Key (Authenticated)
Requires a Bearer token.
```
POST /v1/auth/configure
{
  "gateway_key": "your_gateway_key"
}
```

### Onboarding Lead
```
POST /v1/onboard
{
  "business_name": "Acme Corp",
  "contact_name": "John Doe",
  "email": "john@acme.com",
  "phone": "555-1234",
  "business_type": "retail"
}
```

## Transaction Types

### Sale (Direct Charge)
Charges a vaulted/tokenized card.
```
POST /v1/payments/charge
{
  "amount": 10.00,
  "token": "<vault_token>",
  "description": "Order #1234"
}
```

### 3D Secure
Enable 3DS by sending `three_d_secure: true` on a charge request.
The response includes a `three_d_secure` field confirming it was used.
Use 3DS for higher-value or flagged transactions.

### Refund
```
POST /v1/payments/refund
{
  "transaction_id": "<transaction_id>",
  "amount": 5.00  // omit for full refund
}
```

### Void (Cancel Before Settlement)
```
POST /v1/payments/void
{
  "transaction_id": "<transaction_id>"
}
```

### Invoice / Payment Link
Sends a secure payment link to the customer's email. Card data is entered on a PCI-compliant hosted form — never touches the agent.
```
POST /v1/payments/invoice
{
  "amount": 500.00,
  "email": "customer@example.com",
  "description": "Consulting — January"
}
```

## Customer Vault (Tokenization)

### Add Customer
Creates a customer record for secure card storage.
```
POST /v1/vault/add
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@example.com"
}
```
Returns a vault token ID. The customer enters card details through a secure hosted form.

### Charge Vaulted Customer
```
POST /v1/vault/charge
{
  "vault_id": "<vault_token>",
  "amount": 99.00,
  "description": "Monthly service"
}
```

## Recurring Billing

### Create Subscription
```
POST /v1/subscriptions
{
  "vault_id": "<vault_token>",
  "plan_id": "monthly_99",
  "amount": 99.00,
  "interval": "monthly"
}
```

### Cancel Subscription
```
DELETE /v1/subscriptions/<subscription_id>
```

## Transaction History

### List Transactions
```
GET /v1/transactions
```

### Sales Summary
```
GET /v1/transactions/summary
```

## Fraud Detection & Rules

### Fraud Summary (30-day analytics)
```
GET /v1/fraud/summary
```
Returns transaction count, flagged count, blocked count, active rules, and fraud rate.

### List Fraud Rules
```
GET /v1/fraud/rules
```

### Get Specific Rule
```
GET /v1/fraud/rules/<rule_id>
```

### Create Fraud Rule
```
POST /v1/fraud/rules
{
  "rule_type": "max_amount",   // max_amount | min_amount | velocity_limit
  "threshold": "5000",
  "action": "flag"             // flag (alert) | block (reject) | review (hold)
}
```

### Delete Fraud Rule
```
DELETE /v1/fraud/rules/<rule_id>
```
Note: updates are not supported — delete and recreate instead.

## Response Codes
- **200** — Success (transaction processed, data returned)
- **400** — Bad request (validation error, declined payment, gateway not configured)
- **401** — Unauthorized (missing or expired JWT)
- **404** — Not found (transaction doesn't exist or doesn't belong to you)
- **429** — Rate limited (too many requests)
- **500** — Server error

## Authentication
All endpoints (except register, login, and onboard) require a JWT bearer token:
```
Authorization: Bearer <your_jwt_token>
```
Tokens expire after 24 hours. Re-login to refresh.
