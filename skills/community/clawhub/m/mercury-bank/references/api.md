# Mercury API Reference

Base URL: `https://api.mercury.com/api/v1`
Auth: Basic Auth — token as username, empty password.

```bash
curl --user "$MERCURY_API_TOKEN:" "https://api.mercury.com/api/v1/..."
```

## Endpoints

### Accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List all accounts |
| GET | /account/{id} | Get account by ID |
| GET | /account/{id}/transactions | Account transactions |
| GET | /account/{id}/statements | Account statements |
| GET | /account/{id}/cards | Account cards |

### Transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | All transactions (filterable) |
| GET | /transaction/{id} | Transaction by ID |
| POST | /account/{id}/transactions | Send money |
| POST | /account/{id}/request-send-money | Request send (safe mode) |

### Recipients
| Method | Path | Description |
|--------|------|-------------|
| GET | /recipients | List recipients |
| GET | /recipient/{id} | Get recipient |
| POST | /recipients | Create recipient |
| POST | /recipient/{id} | Update recipient |

### AR Invoices (Mercury Plus required)
| Method | Path | Description |
|--------|------|-------------|
| GET | /ar/invoices | List invoices |
| POST | /ar/invoices | Create invoice |
| GET | /ar/invoices/{id} | Get invoice |
| POST | /ar/invoices/{id} | Update invoice |
| POST | /ar/invoices/{id}/cancel | Cancel invoice |
| GET | /ar/invoices/{id}/attachments | List attachments |
| GET | /ar/invoices/{id}/pdf | Download PDF |

### AR Customers (Mercury Plus required)
| Method | Path | Description |
|--------|------|-------------|
| GET | /ar/customers | List customers |
| POST | /ar/customers | Create customer |
| GET | /ar/customers/{id} | Get customer |

### Organization & Users
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization | Org details |
| GET | /users | List users |
| GET | /users/{id} | Get user |

### Webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks/{id} | Get webhook |
| POST | /webhooks | Create webhook |
| POST | /webhooks/{id} | Update webhook |
| POST | /webhooks/{id}/verify | Verify webhook |

### Events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List events |
| GET | /events/{id} | Get event |

### Treasury
| Method | Path | Description |
|--------|------|-------------|
| GET | /treasury | Treasury account |
| GET | /treasury/{id}/transactions | Treasury transactions |
| GET | /treasury/{id}/statements | Treasury statements |

### SAFEs
| Method | Path | Description |
|--------|------|-------------|
| GET | /safes | List SAFE requests |
| GET | /safes/{id} | Get SAFE by ID |

### Statements
| Method | Path | Description |
|--------|------|-------------|
| GET | /statements/{id}/pdf | Download statement PDF |

## Known Account IDs (D4J LLC)
- Checking ••3223: `4ca92254-e020-11f0-ab61-779167c16d40`
- Savings ••4179: `4cd596f4-e020-11f0-ab61-4b868ee3a466`
- Org ID: `24ff8f74-e019-11f0-9f3c-3b30f2dfe1ae`

## Create Invoice — POST /ar/invoices

```json
{
  "invoiceNumber": "INV-7",
  "invoiceDate": "2026-03-19",
  "dueDate": "2026-03-26",
  "customerId": "<customer-id>",
  "destinationAccountId": "4ca92254-e020-11f0-ab61-779167c16d40",
  "amount": 50000,
  "payerMemo": "Description for payer",
  "achDebitEnabled": true,
  "creditCardEnabled": false
}
```

Note: `amount` is in **cents** (50000 = $500.00).

## Create Customer — POST /ar/customers

```json
{
  "name": "Company Name",
  "email": "billing@company.com",
  "address": {
    "address1": "123 Main St",
    "city": "Houston",
    "region": "TX",
    "postalCode": "77005",
    "country": "US"
  }
}
```

## Send Money — POST /account/{id}/transactions

```json
{
  "recipientId": "<recipient-id>",
  "amount": 50000,
  "paymentMethod": "ach",
  "idempotencyKey": "unique-key-here",
  "note": "Payment note"
}
```
