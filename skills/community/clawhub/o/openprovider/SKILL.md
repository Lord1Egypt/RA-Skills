---
name: openprovider
description: >
  OpenProvider domain registrar & DNS management. Triggers on: register domain,
  buy domain, renew domain, transfer domain, delete domain, restore domain,
  add DNS record, change DNS, create DNS zone, list DNS records, delete DNS zone,
  order SSL certificate, renew SSL, revoke SSL, change nameservers, nameserver group,
  TLD prices, TLD info, WHOIS, domain owner, registrant, customer handle, create contact,
  OpenProvider, Openprovider, domain available, check domain, domain search,
  domain suggestions, bulk domain check, auto-renew, auth code, EPP code, domain status,
  DNS propagation, MX record, SPF record, DKIM record, DMARC record, A record, CNAME record,
  TXT record, reseller, domain pricing, domain cost
---

# OpenProvider Skill

OpenProvider (openprovider.eu) is the domain registrar and DNS provider for Atlas Frontline.
This skill handles all domain, DNS, SSL, and customer handle operations via the
OpenProvider REST API v1beta.

## Auth Flow

**Always obtain a token before making any API call.**

1. Load credentials: `OPENPROVIDER_USERNAME` / `OPENPROVIDER_PASSWORD` (env vars), with legacy fallback from `OPENPROVIDER_USER` / `OPENPROVIDER_PASS`, or DB table `system_settings` (key: `integration_credentials_openprovider`)
2. Get token: `POST https://api.openprovider.eu/v1beta/auth/login`
3. Use token as `Authorization: Bearer {token}` header
4. Token valid for 48h (Atlas caches for 24h)
5. On HTTP 401: invalidate token → re-authenticate → retry request

```bash
# Get token
OP_USER="${OPENPROVIDER_USERNAME:-${OPENPROVIDER_USER:-}}"
OP_PASS="${OPENPROVIDER_PASSWORD:-${OPENPROVIDER_PASS:-}}"
TOKEN=$(curl -s -X POST https://api.openprovider.eu/v1beta/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "'"$OP_USER"'", "password": "'"$OP_PASS"'"}' \
  | jq -r '.data.token')
```

→ Full auth docs: [references/auth.md](references/auth.md)

## API Base

| Setting | Value |
|---------|-------|
| Base URL | `https://api.openprovider.eu/v1beta/` |
| Auth | Bearer Token |
| Content-Type | `application/json` |
| Timeout | 30s |
| Retries | 3 (backoff: 1s, 3s, 9s) |

## Routing Matrix

Use this table to find the right action and reference file:

### Domain Operations

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| Is domain available? / Check domain | `/domains/check` | POST | [domains.md](references/domains.md#check-availability) |
| Register / buy domain | `/domains` | POST | [domains.md](references/domains.md#register-domain) |
| Get domain status | `/domains/{id}` | GET | [domains.md](references/domains.md#get-domain-status) |
| List all domains | `/domains` | GET | [domains.md](references/domains.md#list-domains) |
| Renew domain | `/domains/{id}/renew` | POST | [domains.md](references/domains.md#renew-domain) |
| Update domain settings | `/domains/{id}` | PUT | [domains.md](references/domains.md#update-domain) |
| Transfer domain | `/domains/transfer` | POST | [domains.md](references/domains.md#transfer-domain) |
| Delete / cancel domain | `/domains/{id}` | DELETE | [domains.md](references/domains.md#delete-domain) |
| Restore domain | `/domains/{id}/restore` | POST | [domains.md](references/domains.md#restore-domain) |

### DNS Operations

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| Create DNS zone | `/dns/zones` | POST | [dns.md](references/dns.md#create-dns-zone) |
| Get DNS zone | `/dns/zones/{domain}` | GET | [dns.md](references/dns.md#get-dns-zone) |
| Add/remove DNS records | `/dns/zones/{domain}` | PUT | [dns.md](references/dns.md#update-dns-zone) |
| List DNS records | `/dns/zones/{domain}/records` | GET | [dns.md](references/dns.md#get-dns-records) |
| Delete DNS zone | `/dns/zones/{domain}` | DELETE | [dns.md](references/dns.md#delete-dns-zone) |
| List all DNS zones | `/dns/zones` | GET | [dns.md](references/dns.md#list-dns-zones) |

### SSL Operations

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| Order SSL certificate | `/ssl/orders` | POST | [ssl.md](references/ssl.md#order-ssl-certificate) |
| List SSL certificates | `/ssl/orders` | GET | [ssl.md](references/ssl.md#list-ssl-certificates) |
| Get SSL certificate details | `/ssl/orders/{id}` | GET | [ssl.md](references/ssl.md#get-ssl-certificate) |
| Reissue SSL certificate | `/ssl/orders/{id}/reissue` | POST | [ssl.md](references/ssl.md#reissue-ssl-certificate) |
| Renew SSL certificate | `/ssl/orders/{id}/renew` | POST | [ssl.md](references/ssl.md#renew-ssl-certificate) |
| Cancel SSL certificate | `/ssl/orders/{id}` | DELETE | [ssl.md](references/ssl.md#cancel-ssl-certificate) |
| List SSL products/prices | `/ssl/products` | GET | [ssl.md](references/ssl.md#list-ssl-products) |

### Nameserver Operations

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| List NS groups | `/dns/nameservers/groups` | GET | [nameservers.md](references/nameservers.md#list-nameserver-groups) |
| Get NS group details | `/dns/nameservers/groups/{name}` | GET | [nameservers.md](references/nameservers.md#get-nameserver-group) |
| Create NS group | `/dns/nameservers/groups` | POST | [nameservers.md](references/nameservers.md#create-nameserver-group) |
| Update NS group | `/dns/nameservers/groups/{name}` | PUT | [nameservers.md](references/nameservers.md#update-nameserver-group) |
| Delete NS group | `/dns/nameservers/groups/{name}` | DELETE | [nameservers.md](references/nameservers.md#delete-nameserver-group) |

### TLD Information

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| List all TLDs | `/tlds` | GET | [tlds.md](references/tlds.md#list-tlds) |
| Get TLD details & prices | `/tlds/{name}` | GET | [tlds.md](references/tlds.md#get-tld-details) |

### Customers & Resellers

| Request | Endpoint | Method | Reference |
|---------|----------|--------|-----------|
| List customers | `/customers` | GET | [customers-resellers.md](references/customers-resellers.md#list-customers) |
| Get customer | `/customers/{handle}` | GET | [customers-resellers.md](references/customers-resellers.md#get-customer) |
| Create customer / handle | `/customers` | POST | [customers-resellers.md](references/customers-resellers.md#create-customer) |
| Update customer | `/customers/{handle}` | PUT | [customers-resellers.md](references/customers-resellers.md#update-customer) |
| Delete customer | `/customers/{handle}` | DELETE | [customers-resellers.md](references/customers-resellers.md#delete-customer) |
| Reseller info | `/resellers/{id}` | GET | [customers-resellers.md](references/customers-resellers.md#reseller-information) |

## Workflow: Register Domain (End-to-End)

Full flow when a user says "register the domain example.com":

1. **Check availability** → `POST /domains/check` with `with_price: true`
2. **Ensure customer handle** → `GET /customers` or `POST /customers`
3. **Register domain** → `POST /domains` with owner_handle, ns_group
4. **Create DNS zone** → `POST /dns/zones`
5. **Set DNS records** → `PUT /dns/zones/{domain}` (A, MX, SPF, DKIM, DMARC)
6. **Check status** → `GET /domains/{id}`

## Workflow: Change DNS Record

1. **Load current records** → `GET /dns/zones/{domain}/records`
2. **Normalize the record name to zone-relative form**
3. **Remove old record** → `PUT /dns/zones/{domain}` with `records.remove`
4. **Add new record** → `PUT /dns/zones/{domain}` with `records.add`
5. **Verify the resulting record names** → `GET /dns/zones/{domain}/records`

> **Important:** Do NOT combine remove and add in a single PUT call! Two separate calls required (Error 817).

### DNS Record Naming Rule (CRITICAL)

When updating records in zone `/dns/zones/{domain}`, OpenProvider expects the
record `name` in **zone-relative form** for subdomains.

**Use:**
- `phone` for `phone.example.com` in zone `example.com`
- `_dmarc` for `_dmarc.example.com` in zone `example.com`
- `www` for `www.example.com` in zone `example.com`

**Do NOT use the full FQDN as `name` when writing records inside a zone** unless
you have verified OpenProvider expects it for that exact operation.

If you send `phone.example.com` as `name` inside zone `example.com`, OpenProvider may
append the zone again and create the wrong record:
- intended: `phone.example.com`
- accidental result: `phone.example.com.example.com`

### Safe Name Normalization

Before any DNS write:

1. Identify the zone apex, e.g. `example.com`
2. Convert requested host to zone-relative label:
   - `example.com` → apex/root (`""` empty string for OpenProvider zone writes, not the full domain, and not `@` unless explicitly verified)
   - `phone.example.com` → `phone`
   - `_dmarc.example.com` → `_dmarc`
3. Read back the zone records after the write and confirm the final record name is correct

### Apex / Root Record Rule (CRITICAL)

For OpenProvider `PUT /dns/zones/{domain}` writes, the zone apex must be sent as an empty string name:

```json
{
  "name": "",
  "type": "TXT",
  "value": "google-site-verification=...",
  "ttl": 600
}
```

Do not send the full domain name as `name` for apex writes inside the zone payload.
If you send `example.com` as `name` while writing inside zone `example.com`, OpenProvider may create:
- intended: `example.com`
- accidental result: `example.com.example.com`

Also do not assume `@` works for OpenProvider. It may be rejected as an invalid record name.

### Safe DNS Change Pattern

For any add/replace of a record:

1. Read current zone records
2. Check whether the target record already exists
3. If replacing, remove conflicting record first
4. Add the new record using the **zone-relative** `name`
5. Re-read the zone and verify the exact final FQDN
6. Optionally check public resolution separately (`dig`) because provider acceptance ≠ public propagation

### MX / Mail Provider Rule (CRITICAL)

For OpenProvider DNS writes, MX records use the field name `prio`, not `priority`.

Correct example for a mail subdomain inside zone `example.com`:

```json
{
  "records": {
    "add": [
      {
        "name": "send",
        "type": "MX",
        "value": "feedback-smtp.eu-west-1.amazonses.com",
        "ttl": 600,
        "prio": 10
      }
    ]
  }
}
```

Do not use `priority` in the payload unless you have verified a different endpoint/schema.

For Resend/Amazon SES sender domains, a known-good public result is:

```bash
dig +short MX send.example.com
# 10 feedback-smtp.eu-west-1.amazonses.com.
```

### Example

Zone: `example.com`

Correct add payload for `phone.example.com`:

```json
{
  "records": {
    "add": [
      {
        "name": "phone",
        "type": "A",
        "value": "46.225.220.40",
        "ttl": 900
      }
    ]
  }
}
```

Incorrect payload:

```json
{
  "records": {
    "add": [
      {
        "name": "phone.example.com",
        "type": "A",
        "value": "46.225.220.40",
        "ttl": 900
      }
    ]
  }
}
```

That incorrect payload can create `phone.example.com.example.com`.

Apex TXT example for `example.com`:

Correct:

```json
{
  "records": {
    "add": [
      {
        "name": "",
        "type": "TXT",
        "value": "google-site-verification=...",
        "ttl": 600
      }
    ]
  }
}
```

Incorrect:

```json
{
  "records": {
    "add": [
      {
        "name": "example.com",
        "type": "TXT",
        "value": "google-site-verification=...",
        "ttl": 600
      }
    ]
  }
}
```

That incorrect payload can create `example.com.example.com`.

## Workflow: Domain Transfer

1. **Get auth code** from current registrar (EPP/transfer code)
2. **Ensure customer handle** → `POST /customers` if needed
3. **Initiate transfer** → `POST /domains/transfer` with auth_code + owner_handle

## Error Handling

All API responses follow this structure:

```json
{"code": 0, "desc": "...", "data": {...}}
```

- `code: 0` = success
- `code: != 0` = error (details in `desc`)
- HTTP 401 = token expired → re-authenticate
- HTTP 429 = rate limit → wait and retry
- If env lookup fails, check whether the instance still uses legacy names `OPENPROVIDER_USER` / `OPENPROVIDER_PASS`

Common errors:

| Code | Meaning | Solution |
|------|---------|----------|
| 817 | Duplicate DNS record | Remove existing record first, then add new one |
| 816 | Validation error / invalid field value | Re-check record schema; for MX use `prio` instead of `priority` |
| 801 | Domain already exists | Domain is already registered |
| 899 | Rate limit | Reduce batch size, wait |
| 1000 | Auth failed | Check credentials |

→ Full error reference: [references/auth.md](references/auth.md#common-error-codes)

## Atlas Integration (Context)

OpenProvider is integrated into Atlas via the Frontline module:

- **Service:** `api/services/frontline/openprovider.ts` — API client
- **DNS:** `api/services/frontline/dns.ts` — DNS configuration & verification
- **Handles:** `api/services/frontline/handles.ts` — Workspace handle management
- **Search:** `api/services/frontline/domain-search.ts` — Domain availability search
- **Domains:** `api/services/frontline/domains.ts` — Domain lifecycle
- **Types:** `shared/types/frontline.ts` — TypeScript definitions
- **Credentials:** `system_settings` table, key `integration_credentials_openprovider`

## Key Limits

| Limit | Value |
|-------|-------|
| Domain check batch size | Max 5 per request |
| Suggestions per search | Max 20 |
| Token validity | 48h (cache: 24h) |
| Request timeout | 30s |
| DNS TTL minimum | 600s |
| Domain registrations per workspace/day | Max 3 (Atlas limit) |

## Reference Files

| File | Contents |
|------|----------|
| [references/auth.md](references/auth.md) | Authentication, tokens, credentials, error handling |
| [references/domains.md](references/domains.md) | Domain CRUD, check, transfer, renew, restore |
| [references/dns.md](references/dns.md) | DNS zones & records (CRUD, patterns, pitfalls) |
| [references/ssl.md](references/ssl.md) | SSL certificates (order, reissue, renew, cancel) |
| [references/nameservers.md](references/nameservers.md) | Nameserver group management |
| [references/tlds.md](references/tlds.md) | TLD information & pricing |
| [references/customers-resellers.md](references/customers-resellers.md) | Customer handles & reseller info |
