# OpenProvider — SSL Certificate Operations

> **Atlas Status:** SSL endpoints are NOT yet implemented in Atlas. These are documented from the OpenProvider API for future use.

## Table of Contents

- [List SSL Certificates](#list-ssl-certificates)
- [Order SSL Certificate](#order-ssl-certificate)
- [Get SSL Certificate](#get-ssl-certificate)
- [Reissue SSL Certificate](#reissue-ssl-certificate)
- [Renew SSL Certificate](#renew-ssl-certificate)
- [Cancel SSL Certificate](#cancel-ssl-certificate)
- [List SSL Products](#list-ssl-products)

---

## List SSL Certificates

### GET /ssl/orders

List all SSL certificate orders.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/ssl/orders`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page |
| `offset` | integer | Pagination offset |
| `status` | string | Filter: `active`, `pending`, `cancelled`, `expired` |
| `order_by` | string | Sort field |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/ssl/orders?limit=50&status=active" \
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
        "id": 123456,
        "common_name": "example.com",
        "product_id": 1,
        "status": "active",
        "order_date": "2026-01-15",
        "expiration_date": "2027-01-15",
        "brand_name": "Sectigo"
      }
    ],
    "total": 5
  }
}
```

---

## Order SSL Certificate

### POST /ssl/orders

Order a new SSL certificate.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/ssl/orders`

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `product_id` | integer | SSL product ID (from `/ssl/products`) |
| `period` | integer | Period in years (1, 2, or 3) |
| `csr` | string | Certificate Signing Request (PEM format) |
| `domain_validation_methods` | object | DCV method per domain |
| `organization_handle` | string | Organization contact handle |
| `approver_email` | string | Email for domain validation |

**Request:**

```json
{
  "product_id": 1,
  "period": 1,
  "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...\n-----END CERTIFICATE REQUEST-----",
  "domain_validation_methods": {
    "example.com": "dns"
  },
  "organization_handle": "ORG000001-XX",
  "approver_email": "admin@example.com",
  "software_id": 37
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/ssl/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "period": 1,
    "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...\n-----END CERTIFICATE REQUEST-----",
    "domain_validation_methods": {"example.com": "dns"},
    "approver_email": "admin@example.com"
  }'
```

**Domain Validation Methods:** `email`, `dns`, `http`, `https`

---

## Get SSL Certificate

### GET /ssl/orders/{id}

Get details of a specific SSL order.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/ssl/orders/{id}`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/ssl/orders/123456 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Reissue SSL Certificate

### POST /ssl/orders/{id}/reissue

Reissue an existing certificate (e.g. after key compromise or domain change).

**Endpoint:** `POST https://api.openprovider.eu/v1beta/ssl/orders/{id}/reissue`

**Request:**

```json
{
  "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...\n-----END CERTIFICATE REQUEST-----",
  "domain_validation_methods": {
    "example.com": "dns"
  }
}
```

---

## Renew SSL Certificate

### POST /ssl/orders/{id}/renew

Renew an SSL certificate before expiration.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/ssl/orders/{id}/renew`

**Request:**

```json
{
  "period": 1,
  "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...\n-----END CERTIFICATE REQUEST-----"
}
```

---

## Cancel SSL Certificate

### DELETE /ssl/orders/{id}

Cancel an SSL certificate order.

**Endpoint:** `DELETE https://api.openprovider.eu/v1beta/ssl/orders/{id}`

**curl Example:**

```bash
curl -X DELETE https://api.openprovider.eu/v1beta/ssl/orders/123456 \
  -H "Authorization: Bearer $TOKEN"
```

---

## List SSL Products

### GET /ssl/products

List available SSL products with pricing.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/ssl/products`

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/ssl/products?limit=100" \
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
        "id": 1,
        "name": "PositiveSSL",
        "brand_name": "Sectigo",
        "validation_type": "DV",
        "number_of_domains": 1,
        "prices": { "1": { "price": 5.99, "currency": "EUR" } }
      }
    ]
  }
}
```
