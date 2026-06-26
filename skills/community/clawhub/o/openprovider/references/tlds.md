# OpenProvider — TLD Information & Pricing

> **Atlas Status:** TLD lookups are NOT yet implemented. Atlas uses a hardcoded list of TLDs for domain suggestions. Documented here for future use.

---

## List TLDs

### GET /tlds

List all available TLDs with pricing and requirements.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/tlds`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page |
| `offset` | integer | Pagination offset |
| `name_pattern` | string | Filter by TLD name (e.g. `com`, `de`) |
| `order_by` | string | Sort field: `name`, `price` |
| `status` | string | `active`, `new`, `promo` |
| `with_price` | boolean | Include pricing info |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/tlds?limit=50&with_price=true&status=active" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "results": [
      {
        "name": "com",
        "status": "active",
        "is_transfer_supported": true,
        "is_trade_supported": true,
        "renewal_is_possible": true,
        "min_period": 1,
        "max_period": 10,
        "prices": {
          "create": { "price": 8.99, "currency": "EUR" },
          "transfer": { "price": 8.99, "currency": "EUR" },
          "renew": { "price": 8.99, "currency": "EUR" },
          "restore": { "price": 79.00, "currency": "EUR" }
        }
      }
    ],
    "total": 800
  }
}
```

---

## Get TLD Details

### GET /tlds/{name}

Get detailed information about a specific TLD, including registration requirements.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/tlds/{name}`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/tlds/de \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "name": "de",
    "status": "active",
    "is_transfer_supported": true,
    "min_period": 1,
    "max_period": 1,
    "grace_period": 30,
    "redemption_period": 30,
    "owner_handle_supported": true,
    "admin_handle_supported": true,
    "tech_handle_supported": true,
    "dnssec_supported": true,
    "restrictions": "Owner must have a valid address in any country.",
    "additional_data": []
  }
}
```

---

## Atlas Hardcoded TLDs

Atlas currently uses a static list for domain suggestions instead of querying the TLD API:

```
com, de, io, co, net, org, email, dev, agency, online, tech, biz, pro, ai
```

**Future improvement:** Query `/tlds` for dynamic TLD availability and pricing in domain search suggestions.
