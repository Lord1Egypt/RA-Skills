# OpenProvider — DNS Zone & Record Management

## Table of Contents

- [Create DNS Zone](#create-dns-zone)
- [Get DNS Zone](#get-dns-zone)
- [Update DNS Zone (Add/Remove Records)](#update-dns-zone)
- [Get DNS Records](#get-dns-records)
- [Delete DNS Zone](#delete-dns-zone)
- [List DNS Zones](#list-dns-zones)
- [Record Types & Formats](#record-types--formats)
- [Common Patterns](#common-patterns)
- [Pitfalls](#pitfalls)

---

## Create DNS Zone

### POST /dns/zones

Create a new DNS zone. Required before adding records.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/dns/zones`

**Request:**

```json
{
  "domain": { "name": "example", "extension": "com" },
  "type": "master"
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/dns/zones \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": {"name": "example", "extension": "com"},
    "type": "master"
  }'
```

**Notes:**
- Zone may already exist (returns error) — safe to ignore and proceed with record updates
- Type is always `master` for zones managed by OpenProvider DNS

---

## Get DNS Zone

### GET /dns/zones/{domain}

Get zone metadata (not records — use `/records` for that).

**Endpoint:** `GET https://api.openprovider.eu/v1beta/dns/zones/{domain}`

**Path Parameter:** `domain` — Full domain name (e.g. `example.com`)

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/dns/zones/example.com \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "id": 98765,
    "name": "example.com",
    "type": "master",
    "active": true,
    "creation_date": "2026-04-05T12:00:00Z",
    "modification_date": "2026-04-05T14:30:00Z"
  }
}
```

---

## Update DNS Zone

### PUT /dns/zones/{domain}

Add or remove DNS records on an existing zone. This is the primary method for managing records.

**Endpoint:** `PUT https://api.openprovider.eu/v1beta/dns/zones/{domain}`

### Critical naming rule

For record writes, OpenProvider expects the record `name` in **zone-relative form** for subdomains.

Examples for zone `example.com`:
- apex/root record → `""` (or provider-specific root handling)
- `phone.example.com` → `"phone"`
- `_dmarc.example.com` → `"_dmarc"`
- `www.example.com` → `"www"`

Do **not** send the full host name as `name` when writing records inside an existing zone unless you have confirmed that exact endpoint requires FQDN input.

If you send `phone.example.com` as `name` inside zone `example.com`, OpenProvider may append the zone again and create:
- intended: `phone.example.com`
- accidental: `phone.example.com.example.com`

### Add Records

```json
{
  "records": {
    "add": [
      { "type": "A", "name": "", "value": "1.2.3.4", "ttl": 3600 },
      { "type": "A", "name": "mail", "value": "1.2.3.4", "ttl": 3600 },
      { "type": "MX", "name": "", "value": "mail.example.com", "ttl": 3600, "prio": 10 },
      { "type": "TXT", "name": "", "value": "\"v=spf1 ip4:1.2.3.4 -all\"", "ttl": 3600 }
    ]
  }
}
```

### Remove Records

```json
{
  "records": {
    "remove": [
      { "type": "A", "name": "", "value": "1.2.3.4", "ttl": 3600 }
    ]
  }
}
```

### curl Example (add records):

```bash
curl -X PUT https://api.openprovider.eu/v1beta/dns/zones/example.com \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": {
      "add": [
        {"type": "A", "name": "", "value": "1.2.3.4", "ttl": 3600},
        {"type": "MX", "name": "", "value": "mail.example.com", "ttl": 3600, "prio": 10}
      ]
    }
  }'
```

### curl Example (remove + add = replace):

```bash
# Step 1: Remove old records
curl -X PUT https://api.openprovider.eu/v1beta/dns/zones/example.com \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"records": {"remove": [{"type": "A", "name": "", "value": "OLD_IP", "ttl": 3600}]}}'

# Step 2: Add new records
curl -X PUT https://api.openprovider.eu/v1beta/dns/zones/example.com \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"records": {"add": [{"type": "A", "name": "", "value": "NEW_IP", "ttl": 3600}]}}'
```

### Safe replace flow for subdomains

When replacing a subdomain record:

1. Read current records via `GET /dns/zones/{domain}/records`
2. Find the target FQDN in the response
3. Convert it back to the zone-relative `name` before writing
4. Remove the old record in one PUT
5. Add the new record in a second PUT
6. Re-read records and confirm the final FQDN is correct
7. Optionally verify public propagation with `dig`

Example for zone `example.com` and host `phone.example.com`:
- GET response name: `phone.example.com`
- PUT write name: `phone`

---

## Get DNS Records

### GET /dns/zones/{domain}/records

Get all DNS records for a zone.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/dns/zones/{domain}/records`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/dns/zones/example.com/records \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "results": [
      { "type": "A", "name": "example.com", "value": "1.2.3.4", "ttl": 3600 },
      { "type": "A", "name": "mail.example.com", "value": "1.2.3.4", "ttl": 3600 },
      { "type": "MX", "name": "example.com", "value": "mail.example.com", "ttl": 3600, "prio": 10 },
      { "type": "TXT", "name": "example.com", "value": "\"v=spf1 ip4:1.2.3.4 -all\"", "ttl": 3600 }
    ],
    "total": 4
  }
}
```

**Important:** GET returns FQDN names (e.g. `mail.example.com`), but PUT expects relative names (e.g. `mail`) for subdomain writes. Always normalize when replacing records.

### Name normalization cheat sheet

For zone `example.com`:
- `example.com` → `""`
- `www.example.com` → `"www"`
- `mail.example.com` → `"mail"`
- `_dmarc.example.com` → `"_dmarc"`

Never copy the GET `name` field directly into a PUT payload for subdomain writes without stripping the zone suffix first.

---

## Delete DNS Zone

### DELETE /dns/zones/{domain}

Delete an entire DNS zone and all its records.

**Endpoint:** `DELETE https://api.openprovider.eu/v1beta/dns/zones/{domain}`

**curl Example:**

```bash
curl -X DELETE https://api.openprovider.eu/v1beta/dns/zones/example.com \
  -H "Authorization: Bearer $TOKEN"
```

> **Warning:** This removes ALL records. There is no undo.

---

## List DNS Zones

### GET /dns/zones

List all DNS zones in the account.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/dns/zones`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page |
| `offset` | integer | Pagination offset |
| `name_pattern` | string | Wildcard search |
| `type` | string | `master` or `slave` |
| `order_by` | string | Sort field |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/dns/zones?limit=50&type=master" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Record Types & Formats

| Type | `name` field | `value` field | `prio` | Notes |
|------|-------------|---------------|--------|-------|
| A | `""` (root) or subdomain | IPv4 address | — | |
| AAAA | `""` or subdomain | IPv6 address | — | |
| MX | `""` or subdomain | Mail server FQDN | Required (e.g. 10) | Use `prio`, **not** `priority` |
| TXT | `""` or subdomain | Quoted string | — | Wrap in `"\"...\""` |
| CNAME | subdomain | Target FQDN | — | Cannot be on root |
| NS | `""` or subdomain | Nameserver FQDN | — | |
| SRV | `_service._proto` | `weight port target` | Required | |
| CAA | `""` or subdomain | `flag tag value` | — | |

**TXT value quoting:** OpenProvider expects TXT values wrapped in escaped quotes: `"\"v=spf1 ...\""`

**MX priority field:** OpenProvider expects the field name `prio` in write payloads. `priority` can be rejected with validation errors.

**TTL minimum:** 600 seconds (OpenProvider enforces this; lower values are rejected)

---

## Common Patterns

### Full Email Domain Setup (Atlas Frontline)

Atlas configures these records for outreach domains:

```json
{
  "records": {
    "add": [
      { "type": "A", "name": "", "value": "{IP}", "ttl": 3600 },
      { "type": "A", "name": "mail", "value": "{IP}", "ttl": 3600 },
      { "type": "MX", "name": "", "value": "mail.{domain}", "ttl": 3600, "prio": 10 },
      { "type": "TXT", "name": "", "value": "\"v=spf1 ip4:{IP} -all\"", "ttl": 3600 },
      { "type": "TXT", "name": "{selector}._domainkey", "value": "\"{DKIM_KEY}\"", "ttl": 3600 },
      { "type": "TXT", "name": "_dmarc", "value": "\"v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@lynk.run\"", "ttl": 3600 }
    ]
  }
}
```

### Add a Single Record

```json
{
  "records": {
    "add": [
      { "type": "CNAME", "name": "www", "value": "example.com", "ttl": 3600 }
    ]
  }
}
```

### Resend / Amazon SES Domain Verification (Known-Good Pattern)

For a sender subdomain like `send.example.com` in zone `example.com`, use **relative** names and OpenProvider's native MX field names:

```json
{
  "records": {
    "add": [
      {
        "type": "MX",
        "name": "send",
        "value": "feedback-smtp.eu-west-1.amazonses.com",
        "ttl": 600,
        "prio": 10
      },
      {
        "type": "TXT",
        "name": "send",
        "value": "\"v=spf1 include:amazonses.com ~all\"",
        "ttl": 600
      },
      {
        "type": "TXT",
        "name": "resend._domainkey",
        "value": "\"p=MI...\"",
        "ttl": 600
      },
      {
        "type": "TXT",
        "name": "_dmarc",
        "value": "\"v=DMARC1; p=none;\"",
        "ttl": 600
      }
    ]
  }
}
```

Expected public result:

```bash
dig +short MX send.example.com
# 10 feedback-smtp.eu-west-1.amazonses.com.
```

---

## Pitfalls

1. **Duplicate record error (817):** OpenProvider does NOT process `remove` and `add` atomically in one PUT. Sending both in one call causes Error 817. Always use two separate PUT calls: remove first, then add.

2. **FQDN vs. relative names:** GET returns FQDN (`mail.example.com`), PUT expects relative (`mail`) for subdomain writes. Strip the zone suffix before building PUT payloads. Do not paste a GET name directly into a write payload unless it is the apex/root case.

   Real failure mode:
   - zone: `example.com`
   - intended host: `phone.example.com`
   - wrong PUT name: `phone.example.com`
   - possible result: `phone.example.com.example.com`

3. **Zone creation idempotency:** Creating an already-existing zone returns an error. This is safe to ignore — proceed with record operations.

4. **TTL minimum 600:** Setting TTL below 600 causes a validation error.

5. **TXT quoting:** Values must be wrapped in escaped double quotes in the JSON body.

6. **MX priority field name:** For OpenProvider DNS writes, use `prio` instead of `priority`. A payload that uses `priority` can fail even when the numeric value itself is correct.

7. **Resend / SES subdomain pattern:** For `send.example.com` inside zone `example.com`, write `name: "send"`, not the full FQDN. Public verification should show `10 feedback-smtp.<region>.amazonses.com.`
