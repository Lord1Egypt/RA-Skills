# OpenProvider — Customer & Reseller Management

## Table of Contents

- [List Customers](#list-customers)
- [Get Customer](#get-customer)
- [Create Customer](#create-customer)
- [Update Customer](#update-customer)
- [Delete Customer](#delete-customer)
- [Customer Data Structure](#customer-data-structure)
- [Reseller Information](#reseller-information)

---

## List Customers

### GET /customers

List all customer handles. Used for domain registrant management.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/customers`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page (default 100) |
| `offset` | integer | Pagination offset |
| `order_by` | string | Sort field: `handle`, `company_name`, `last_name` |
| `order` | string | `ASC` or `DESC` |
| `email_pattern` | string | Filter by email |
| `last_name_pattern` | string | Filter by last name |
| `company_name_pattern` | string | Filter by company |
| `handle_pattern` | string | Filter by handle ID |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/customers?limit=100&order_by=handle&order=ASC" \
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
        "handle": "JD000001-XX",
        "name": {
          "company_name": "Acme GmbH",
          "first_name": "John",
          "last_name": "Doe"
        },
        "email": "john@acme.com",
        "phone": {
          "country_code": "+49",
          "area_code": "30",
          "subscriber_number": "12345678"
        },
        "status": "ACT"
      }
    ],
    "total": 15
  }
}
```

---

## Get Customer

### GET /customers/{handle}

Get details of a specific customer handle.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/customers/{handle}`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/customers/JD000001-XX \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "handle": "JD000001-XX",
    "name": {
      "company_name": "Acme GmbH",
      "first_name": "John",
      "last_name": "Doe"
    },
    "email": "john@acme.com",
    "phone": {
      "country_code": "+49",
      "area_code": "30",
      "subscriber_number": "12345678"
    },
    "address": {
      "street": "Musterstr.",
      "number": "42",
      "city": "Berlin",
      "zipcode": "10115",
      "country": "DE",
      "state": ""
    },
    "vat": "DE123456789",
    "status": "ACT"
  }
}
```

---

## Create Customer

### POST /customers

Create a new customer handle (registrant profile) for domain registration.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/customers`

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `company_name` | string | Organization name |
| `name.first_name` | string | First name |
| `name.last_name` | string | Last name |
| `email` | string | Contact email |
| `phone` | object | Phone number (see structure below) |
| `address` | object | Full address |

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `vat` | string | VAT number (e.g. `DE123456789`) |
| `address.state` | string | State/province |

**Request:**

```json
{
  "company_name": "Acme GmbH",
  "name": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "email": "john@acme.com",
  "phone": {
    "country_code": "+49",
    "area_code": "30",
    "subscriber_number": "12345678"
  },
  "address": {
    "street": "Musterstr.",
    "number": "42",
    "city": "Berlin",
    "zipcode": "10115",
    "country": "DE",
    "state": ""
  },
  "vat": "DE123456789"
}
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "handle": "JD000001-XX"
  }
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/customers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme GmbH",
    "name": {"first_name": "John", "last_name": "Doe"},
    "email": "john@acme.com",
    "phone": {"country_code": "+49", "area_code": "30", "subscriber_number": "12345678"},
    "address": {"street": "Musterstr.", "number": "42", "city": "Berlin", "zipcode": "10115", "country": "DE"}
  }'
```

**Note:** If a customer with the same email already exists, OpenProvider may return the existing handle instead of creating a duplicate.

---

## Update Customer

### PUT /customers/{handle}

Update an existing customer handle.

**Endpoint:** `PUT https://api.openprovider.eu/v1beta/customers/{handle}`

**Request (partial update):**

```json
{
  "email": "new-email@acme.com",
  "address": {
    "street": "Neue Str.",
    "number": "10",
    "city": "München",
    "zipcode": "80331",
    "country": "DE"
  }
}
```

**curl Example:**

```bash
curl -X PUT https://api.openprovider.eu/v1beta/customers/JD000001-XX \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "new-email@acme.com"}'
```

---

## Delete Customer

### DELETE /customers/{handle}

Delete a customer handle. Cannot delete handles assigned to active domains.

**Endpoint:** `DELETE https://api.openprovider.eu/v1beta/customers/{handle}`

**curl Example:**

```bash
curl -X DELETE https://api.openprovider.eu/v1beta/customers/JD000001-XX \
  -H "Authorization: Bearer $TOKEN"
```

---

## Customer Data Structure

### Phone Number Format

OpenProvider expects structured phone numbers:

```json
{
  "country_code": "+49",
  "area_code": "30",
  "subscriber_number": "12345678"
}
```

Atlas uses `parsePhoneForOpenprovider()` (from `api/services/core/phone.ts`) to convert flat phone strings to this format. Supported countries include DE, US, PT, NL, GB, FR, AT, CH, and more.

### Address Format

```json
{
  "street": "Musterstr.",
  "number": "42",
  "city": "Berlin",
  "zipcode": "10115",
  "country": "DE",
  "state": ""
}
```

`country` must be an ISO 3166-1 alpha-2 code (e.g. `DE`, `US`, `NL`).

### Atlas DomainOwnerInfo Mapping

Atlas stores registrant info as `DomainOwnerInfo`, which maps to OpenProvider fields:

| Atlas Field | OpenProvider Field |
|-------------|-------------------|
| `first_name` | `name.first_name` |
| `last_name` | `name.last_name` |
| `organization` | `company_name` |
| `email` | `email` |
| `phone` | `phone` (parsed) |
| `street` | `address.street` |
| `house_number` | `address.number` |
| `city` | `address.city` |
| `postal_code` | `address.zipcode` |
| `country` | `address.country` |
| `state` | `address.state` |
| `vat` | `vat` |

---

## Reseller Information

The `reseller_id` is returned during authentication (`POST /auth/login`). It identifies the reseller account.

### GET /resellers/{id}

Get reseller account details.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/resellers/{id}`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/resellers/123456 \
  -H "Authorization: Bearer $TOKEN"
```

This returns account balance, contact info, and configuration. Useful for checking account credit before domain operations.
