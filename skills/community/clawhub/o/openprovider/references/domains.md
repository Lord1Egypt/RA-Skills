# OpenProvider — Domain Operations

## Table of Contents

- [Check Availability](#check-availability)
- [Register Domain](#register-domain)
- [Get Domain Status](#get-domain-status)
- [Renew Domain](#renew-domain)
- [List Domains](#list-domains)
- [Update Domain](#update-domain)
- [Transfer Domain](#transfer-domain)
- [Delete Domain](#delete-domain)
- [Restore Domain](#restore-domain)
- [Domain Suggestions (Atlas)](#domain-suggestions-atlas)
- [Status Codes](#status-codes)

---

## Check Availability

### POST /domains/check

Check if one or more domains are available for registration. Supports bulk checking with pricing.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/domains/check`

**Request:**

```json
{
  "domains": [
    { "name": "example", "extension": "com" },
    { "name": "example", "extension": "de" },
    { "name": "example", "extension": "io" }
  ],
  "with_price": true
}
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "results": [
      {
        "domain": "example.com",
        "status": "free",
        "price": {
          "product": 9.99,
          "currency": "EUR"
        }
      },
      {
        "domain": "example.de",
        "status": "active",
        "price": null
      }
    ]
  }
}
```

**Status values:** `free` (available) | `active` (taken)

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/domains/check \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domains": [{"name": "example", "extension": "com"}],
    "with_price": true
  }'
```

**Limits:**
- Max 5 domains per request (OpenProvider rejects larger batches)
- Atlas batches in groups of 5 for bulk checks

---

## Register Domain

### POST /domains

Register a new domain. Requires an existing customer handle as the owner.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/domains`

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `domain.name` | string | Domain name without extension |
| `domain.extension` | string | TLD (e.g. `com`, `de`) |
| `owner_handle` | string | Customer handle (e.g. `JD000001-XX`) |
| `admin_handle` | string | Admin contact handle |
| `tech_handle` | string | Technical contact handle |

**Optional Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | integer | 1 | Registration period in years |
| `autorenew` | string | `"on"` | Auto-renewal: `"on"` or `"off"` |
| `ns_group` | string | — | Nameserver group (Atlas uses `"dns-openprovider"`) |
| `ns_template_name` | string | — | Nameserver template name |

**Request:**

```json
{
  "domain": { "name": "example", "extension": "com" },
  "owner_handle": "JD000001-XX",
  "admin_handle": "JD000001-XX",
  "tech_handle": "JD000001-XX",
  "period": 1,
  "autorenew": "on",
  "ns_group": "dns-openprovider"
}
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "id": 12345678,
    "status": "REQ",
    "auth_code": "abc123xyz",
    "activation_date": "2026-04-05T12:00:00Z",
    "expiration_date": "2027-04-05T12:00:00Z"
  }
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/domains \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": {"name": "example", "extension": "com"},
    "owner_handle": "JD000001-XX",
    "admin_handle": "JD000001-XX",
    "tech_handle": "JD000001-XX",
    "period": 1,
    "autorenew": "on",
    "ns_group": "dns-openprovider"
  }'
```

---

## Get Domain Status

### GET /domains/{id}

Retrieve current status and details of a registered domain.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/domains/{id}`

**Path Parameter:** `id` — OpenProvider domain ID (integer)

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "id": 12345678,
    "status": "ACT",
    "domain": { "name": "example", "extension": "com" },
    "expiration_date": "2027-04-05T12:00:00Z",
    "renewal_date": "2027-03-05T12:00:00Z",
    "auto_renew": true
  }
}
```

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/domains/12345678 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Renew Domain

### POST /domains/{id}/renew

Renew a domain for a specified period.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/domains/{id}/renew`

**Request:**

```json
{
  "period": 1
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/domains/12345678/renew \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"period": 1}'
```

---

## List Domains

### GET /domains

List all domains in the reseller account. Supports filtering and pagination.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/domains`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page (default: 100) |
| `offset` | integer | Pagination offset |
| `order_by` | string | Sort field: `domain_name`, `expiration_date`, `status` |
| `order` | string | `ASC` or `DESC` |
| `status` | string | Filter by status: `ACT`, `REQ`, `FAI`, `DEL` |
| `domain_name_pattern` | string | Wildcard search (e.g. `*example*`) |
| `extension` | string | Filter by TLD |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/domains?limit=50&status=ACT&order_by=expiration_date&order=ASC" \
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
        "id": 12345678,
        "domain": { "name": "example", "extension": "com" },
        "status": "ACT",
        "expiration_date": "2027-04-05",
        "auto_renew": true,
        "owner_handle": "JD000001-XX"
      }
    ],
    "total": 42
  }
}
```

---

## Update Domain

### PUT /domains/{id}

Update domain settings (autorenew, nameservers, handles).

**Endpoint:** `PUT https://api.openprovider.eu/v1beta/domains/{id}`

**Request (example — toggle autorenew):**

```json
{
  "autorenew": "off"
}
```

**Request (example — change nameservers):**

```json
{
  "ns_group": "dns-openprovider"
}
```

**curl Example:**

```bash
curl -X PUT https://api.openprovider.eu/v1beta/domains/12345678 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"autorenew": "off"}'
```

---

## Transfer Domain

### POST /domains/transfer

Initiate a domain transfer from another registrar.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/domains/transfer`

**Request:**

```json
{
  "domain": { "name": "example", "extension": "com" },
  "auth_code": "transfer-auth-code-from-current-registrar",
  "owner_handle": "JD000001-XX",
  "admin_handle": "JD000001-XX",
  "tech_handle": "JD000001-XX",
  "ns_group": "dns-openprovider"
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/domains/transfer \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": {"name": "example", "extension": "com"},
    "auth_code": "AUTH-CODE-HERE",
    "owner_handle": "JD000001-XX",
    "admin_handle": "JD000001-XX",
    "tech_handle": "JD000001-XX"
  }'
```

---

## Delete Domain

### DELETE /domains/{id}

Request domain deletion. Domain may enter a redemption grace period depending on TLD.

**Endpoint:** `DELETE https://api.openprovider.eu/v1beta/domains/{id}`

**Optional Request Body:**

```json
{
  "type": "default"
}
```

**curl Example:**

```bash
curl -X DELETE https://api.openprovider.eu/v1beta/domains/12345678 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Restore Domain

### POST /domains/{id}/restore

Restore a domain from redemption grace period.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/domains/{id}/restore`

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/domains/12345678/restore \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

> **Note:** Restore fees vary by TLD and can be significantly higher than regular registration.

---

## Domain Suggestions (Atlas)

Atlas generates up to 20 domain name suggestions for availability checking using these patterns:

**Prefixes:** `try`, `get`, `meet`
**Suffixes:** `-sales`, `-reach`, `-mail`, `hq`
**TLDs:** `com`, `de`, `io`, `co`, `net`, `org`, `email`, `dev`, `agency`, `online`, `tech`, `biz`, `pro`, `ai`

Example for base name `acme`:
- `acme.com`, `acme.de`, `acme.io` ...
- `tryacme.com`, `getacme.com`, `meetacme.com` ...
- `acme-sales.com`, `acme-reach.com`, `acme-mail.com`, `acmehq.com` ...

---

## Status Codes

### OpenProvider Domain Status → Atlas Mapping

| OP Status | Meaning | Atlas Status | Sync? |
|-----------|---------|--------------|-------|
| `ACT` | Active (registered, live) | `active` | Yes |
| `REQ` | Requested (pending at registry) | `registering` | No (transient) |
| `FAI` | Failed (registration/transfer) | `suspended` | Yes |
| `DEL` | Deleted | `decommissioned` | Yes |

### Atlas Domain Lifecycle

```
registering → registered → configuring → active
                                        → suspended
                                        → expired
                                        → decommissioned
```
