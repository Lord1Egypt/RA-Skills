# Enable Banking API — Quick Reference

**Base URL:** `https://api.enablebanking.com`  
**Docs:** https://enablebanking.com/docs/api/reference/  
**Auth:** JWT RS256 (Bearer Token)

---

## Authentication

### JWT Structure

**Header:**
```json
{
  "typ": "JWT",
  "alg": "RS256",
  "kid": "<application_id>"
}
```

**Payload:**
```json
{
  "iss": "enablebanking.com",
  "aud": "api.enablebanking.com",
  "iat": 1700000000,
  "exp": 1700086400
}
```

- `iat` = current Unix timestamp
- `exp` = max `iat + 86400` (24 hours)
- `kid` = Application UUID from Developer Portal

**Request Header:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

---

## Endpoints

### ASPSPs (Banks)

#### `GET /aspsps`
List available banks.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `country` | string | ISO 3166-1 alpha-2 (DE, AT, CH, ...) |

**Response:**
```json
[
  {
    "name": "Deutsche Kreditbank AG",
    "country": "DE",
    "logo": "https://...",
    "sandboxMode": true
  }
]
```

---

### Authorization

#### `POST /auth`
Start bank authorization flow.

**Request body:**
```json
{
  "aspsp": {
    "name": "Deutsche Kreditbank AG",
    "country": "DE"
  },
  "state": "unique-state-string",
  "redirect_url": "http://localhost:8888/callback",
  "app": {
    "name": "YourAppName",
    "description": "App description"
  },
  "accounts": [{"iban": null}],
  "scopes": ["aiia.accounts", "aiia.balances", "aiia.transactions"]
}
```

**Response:**
```json
{
  "url": "https://bank.example.com/auth?client_id=...&state=...",
  "state": "unique-state-string"
}
```

User must be redirected to `url`. After login, bank redirects to `redirect_url?code=<code>&state=<state>`.

---

### Sessions

#### `POST /sessions`
Create session after user authorization.

**Request body:**
```json
{
  "code": "<authorization_code_from_callback>"
}
```

**Response:**
```json
{
  "session_id": "uuid-session-id",
  "status": "AUTHORIZED",
  "accounts": [
    {
      "uid": "account-uid-1",
      "iban": "DE89370400440532013000",
      "currency": "EUR",
      "cash_account_type": "CACC",
      "name": "Girokonto"
    }
  ]
}
```

#### `GET /sessions/{session_id}`
Get session details + account list.

**Response:** Same as POST /sessions response.

---

### Accounts

#### `GET /accounts/{account_id}`
Get account details.

**Response:**
```json
{
  "uid": "account-uid",
  "iban": "DE89370400440532013000",
  "currency": "EUR",
  "cash_account_type": "CACC",
  "name": "Girokonto",
  "account_servicer": {
    "bic_fi": "DEUTDEDB"
  }
}
```

---

### Balances

#### `GET /accounts/{account_id}/balances`
Get account balances.

**Response:**
```json
{
  "balances": [
    {
      "balance_type": "CLBD",
      "amount": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "credit_debit_indicator": "CRDT",
      "last_change_date_time": "2024-01-15T10:30:00Z"
    },
    {
      "balance_type": "ITAV",
      "amount": {
        "amount": "1200.00",
        "currency": "EUR"
      },
      "credit_debit_indicator": "CRDT"
    }
  ]
}
```

**Balance types:**
| Code | Description |
|------|-------------|
| `CLBD` | Closing Balance (Buchungssaldo) |
| `ITAV` | Available Balance (Verfügbarer Saldo) |
| `PRCD` | Previously Closed Balance |
| `OTHR` | Other |

---

### Transactions

#### `GET /accounts/{account_id}/transactions`
Get transactions (paginated, 10 per page).

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `date_from` | string | ISO date (YYYY-MM-DD) |
| `date_to` | string | ISO date (YYYY-MM-DD) |
| `continuation_key` | string | Pagination cursor from previous response |

**Response:**
```json
{
  "transactions": [
    {
      "transaction_id": "tx-id-1",
      "booking_date": "2024-01-15",
      "value_date": "2024-01-15",
      "transaction_amount": {
        "amount": "-49.99",
        "currency": "EUR"
      },
      "credit_debit_indicator": "DBIT",
      "remittance_information_unstructured": "REWE KARLSRUHE",
      "creditor_name": "REWE Markt GmbH",
      "creditor_account": {
        "iban": "DE..."
      }
    }
  ],
  "continuation_key": "eyJhbGciOi..."
}
```

**Pagination:** If `continuation_key` is present, add it as query param for next page. No key = last page.

**Transaction fields:**
| Field | Description |
|-------|-------------|
| `booking_date` | Buchungsdatum |
| `value_date` | Wertstellungsdatum |
| `transaction_amount.amount` | Betrag (negativ = Abbuchung) |
| `credit_debit_indicator` | `CRDT` (Gutschrift) / `DBIT` (Lastschrift) |
| `remittance_information_unstructured` | Verwendungszweck (frei) |
| `remittance_information_structured` | Strukturierter Verwendungszweck |
| `creditor_name` | Empfänger (bei DBIT) |
| `debtor_name` | Sender (bei CRDT) |
| `transaction_id` | Bank-interne ID |

---

## Error Codes

| Status | Meaning | Action |
|--------|---------|--------|
| `400` | Bad Request | Check request body/params |
| `401` | Unauthorized | JWT invalid/expired — regenerate |
| `403` | Forbidden | Session expired / consent denied — reconnect |
| `404` | Not Found | Account/session ID invalid |
| `429` | Rate Limited | Check `Retry-After` header, wait |
| `500` | Server Error | Retry after delay |

---

## Sandbox Credentials

### DKB (Deutsche Kreditbank AG)
| Credentials | Accounts |
|-------------|---------|
| user: `aspsp1` / pw: `aspsp1` | 2 Konten |
| user: `aspsp4` / pw: `aspsp4` | 4 Konten |

### Volksbank / Raiffeisenbank
- VR NetKey: `VRK1234567890ALL`
- PIN: `password`
- OTP: `123456`

### Mock ASPSP
- No credentials needed
- Click "Authorize" in the browser

---

## Rate Limits

- Default: ~60 requests/minute
- Transactions: ~30 requests/minute
- 429 responses include `Retry-After` header (seconds)

---

## Scopes

| Scope | Description |
|-------|-------------|
| `aiia.accounts` | Read account info |
| `aiia.balances` | Read balances |
| `aiia.transactions` | Read transactions |

---

## Production — Linked Accounts (MVP)

For production access without a full PSD2 enterprise contract:

1. Register at https://enablebanking.com/developers
2. Create Production application
3. Click **"Activate by linking accounts"**
4. Add your own bank account via the UI
5. App status becomes `Active (restricted)`
6. Can only read data for linked accounts
7. Perfect for MVPs with real client data

> Full PSD2 access (all accounts) requires Enterprise agreement with Enable Banking.
