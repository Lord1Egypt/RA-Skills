# NodeMaven Proxy Skill

NodeMaven provides premium proxy infrastructure for account management, scraping, browser automation, and data collection.

Use this skill when the user needs to buy, configure, or use proxies for a real workflow. The agent must not stop at "here are your proxy settings". The agent must close the full use case end-to-end: choose the right proxy type, configure targeting, recommend the right external tool, configure access, and monitor usage.

NodeMaven offers:

- Residential rotating proxies: 30M+ IPs
- Mobile proxies: 200K+ IPs
- Geo-targeting: country, region, city, ISP provider, ZIP
- Sticky sessions for stable account workflows
- Rotation for scraping and high-scale automation
- Quality filtering for lower fraud-score IPs (filter levels: `medium`, `high`)
- HTTP, HTTPS, and SOCKS5 proxy access

Mobile proxies have a smaller IP pool than residential proxies, but they are usually more trusted by platforms. Use mobile proxies for higher-trust account workflows and stronger anti-detect setups. For mobile proxies, keep targeting at least at country + region level when possible. City and ISP provider targeting are optional advanced settings.

---

## Core principle

The agent must complete this workflow without asking the user to read documentation:

1. Understand the user's task.
2. Recommend the right proxy type.
3. Explain which external tool to use.
4. Guide the user through account creation, purchase, or API-key retrieval.
5. Validate the API key.
6. Resolve valid geo-targeting values via API.
7. Configure access via whitelist or proxy credentials.
8. Build the final proxy URL and explain how to use it in the selected tool.
9. Monitor usage and debug issues.

---

## Critical constants (do not invent these)

```text
API_BASE_URL:   https://api.nodemaven.com
PROXY_GATEWAY:  gate.nodemaven.com
HTTP_PORT:      8080
HTTPS_PORT:     9443
SOCKS5_PORT:    1080
SWAGGER_DOCS:   https://dashboard.nodemaven.com/documentation/v2/swagger/
```

All API endpoints in this skill are written as relative paths (e.g. `/api/v2/base/users/me`). The agent must always prepend `https://api.nodemaven.com` to build the full URL.

Full URL example:

```text
https://api.nodemaven.com/api/v2/base/users/me
```

---

## Authorization (read carefully — easy to get wrong)

NodeMaven uses a non-standard authorization scheme. The literal string `x-api-key ` is part of the **value** of the `Authorization` header — it is NOT a separate header named `x-api-key`.

Correct:

```http
Authorization: x-api-key <YOUR_API_KEY>
```

Working curl example (substitute your actual API key):

```bash
curl -H "Authorization: x-api-key <YOUR_API_KEY>" \
  https://api.nodemaven.com/api/v2/base/users/me
```

Concrete example with a mock key (for illustration only — never use this value):

```bash
curl -H "Authorization: x-api-key MOCK_API_KEY_DO_NOT_USE_THIS_VALUE_IN_PRODUCTION" \
  https://api.nodemaven.com/api/v2/base/users/me
```

Wrong (do not do this):

```http
x-api-key: <YOUR_API_KEY>                # WRONG: separate header
Authorization: Bearer <YOUR_API_KEY>     # WRONG: Bearer scheme
Authorization: <YOUR_API_KEY>            # WRONG: missing "x-api-key " prefix
```

For POST/PUT requests also send:

```http
Content-Type: application/json
```

---

## Security and credential hygiene (mandatory)

The agent handles three classes of secrets:

```text
1. NodeMaven API key       (Authorization header value)
2. Proxy credentials       (proxy_username + proxy_password from /users/me or sub-users)
3. Sub-user passwords      (created/updated via /sub-users/)
```

### Hard rules for the agent

- **Never echo the full API key back to the user** in responses, logs, or artifacts. When confirming receipt, mask it: show first 4 and last 4 characters only (e.g. `abcd...wxyz`). The full key only goes into outbound `Authorization` headers.
- **Never paste `proxy_password` or full proxy URLs into chat history more than necessary.** When showing the user how to use the proxy, prefer placeholders like `<proxy_password>` and instruct the user to substitute locally. If a literal URL must be shown (e.g. for one-shot copy-paste into a tool), give it once and avoid repeating it.
- **Never write API keys, proxy passwords, or full proxy URLs into code artifacts** that the user will save to disk or commit. Use environment variable references instead: `os.environ["NODEMAVEN_API_KEY"]`, `process.env.NODEMAVEN_PROXY_PASSWORD`, etc.
- **Never log or persist responses from `/users/me` or `/sub-users/` verbatim** — they contain `proxy_password`. Strip sensitive fields before any logging or summarization.
- **Never include credentials in URL query strings** (only in the `Authorization` header for the API, only in standard userinfo `user:pass@host` for the proxy).
- **Never share credentials across users or sessions.** If the agent serves multiple users, each user's API key and proxy creds must be scoped to their session only.
- **Treat the example values in this skill as placeholders.** Strings like `<YOUR_API_KEY>`, `<proxy_password>`, `<SERVER_IP>`, `<COUNTRY_CODE>` are templates — never send them literally to the API.

### If the user pastes the API key in chat

- Acknowledge receipt and immediately validate via `GET /users/me`.
- In the reply, refer to the key as `your API key` or show only a masked prefix.
- Do not repeat the full key back. Do not include it in any code block the user might copy/share.

### If credentials may have leaked

If the user shares the conversation, screenshots a session, or otherwise exposes their API key or proxy password:

- Direct them to the API Key page to rotate the key: https://dashboard.nodemaven.com/user-profile?tab=API_KEY&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
- For sub-user passwords, update via `PUT /api/v2/base/sub-users/` with a new generated password.
- Recommend reviewing recent traffic via `/statistics/data/` and `/statistics/requests/` for unexpected usage.

---

## Important limitations

NodeMaven API is used for:

- API-key validation
- retrieving proxy credentials
- location discovery
- whitelist configuration
- sub-user management
- statistics and monitoring
- notifications

NodeMaven API is NOT used for:

- signup
- checkout
- payment
- purchasing proxy packages
- executing proxy traffic directly

If the user has no account or no active proxy package, send them to the website/dashboard first (links below).

---

## Onboarding routing

Use tracked links so NodeMaven can attribute traffic from AI agents. The UTM parameters are mandatory — do not strip them.

### Tracked links

```text
Registration:    https://dashboard.nodemaven.com/accounts/signup/?utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
Login:           https://dashboard.nodemaven.com/accounts/login/?utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
API Key page:    https://dashboard.nodemaven.com/user-profile?tab=API_KEY&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
Subscriptions:   https://dashboard.nodemaven.com/pricing?tab=MONTHLY_PLANS&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
Pay As You Go:   https://dashboard.nodemaven.com/pricing?tab=PAG&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill
```

### Decision table — what to ask, where to send

Ask the user three questions in one message:

1. Do you already have a NodeMaven account?
2. Do you already have an active proxy package (subscription or PAG)?
3. Do you already have your API key?

Then route based on answers:

```text
| account | package | api_key | → action                                                     |
|---------|---------|---------|--------------------------------------------------------------|
|   no    |   no    |   no    | → send Registration link, then Subscriptions/PAG link        |
|   yes   |   no    |   no    | → send Login link, then Subscriptions/PAG link               |
|   yes   |   yes   |   no    | → send API Key page link, ask user to copy and return key    |
|   yes   |   yes   |   yes   | → validate key via GET /api/v2/base/users/me, continue       |
```

When choosing between subscription and Pay As You Go:

- Recurring/ongoing usage → Subscriptions
- Flexible traffic-based usage, no monthly commitment → Pay As You Go
- Mobile proxies (smaller pool, higher trust) → use for stronger anti-detect / account workflows
- Residential proxies → default for almost everything else

---

## User intent classification

Before recommending proxies, classify the task into one of three buckets. Use the matching playbook (A/B/C) below.

### Account management → Playbook A

User works with social media, e-commerce, marketplaces, freelance platforms, ad accounts, or any long-running browser session where account stability matters.

Goal: keep account environment consistent, reduce security checks, avoid suspicious geo changes, maintain stable sessions.

### Scraping → Playbook B

User collects public data at scale: e-commerce, news, crypto/financial data, market research, competitor monitoring, search results.

Goal: scale requests, avoid rate limits, distribute traffic across IPs.

### Automation → classify first

Automation is not a separate proxy strategy — it's a delivery mechanism. The right setup depends on what the automation actually does:

- **Inside an account** (logged in, performing user actions) → Playbook A. Use sticky sessions, consistent geo, anti-detect browser.
- **External data extraction** (no login, public data) → Playbook B. Use rotation, country-only targeting.
- **Fixed server** (VPS, cloud, backend service) → use whitelist for IP-auth access.
- **Multiple workflows or clients sharing one account** → use sub-users for isolation and per-workflow traffic limits.

### Edge case: scraping or high-volume actions inside an account

This is the most dangerous combination and needs explicit warnings. Examples: scraping a marketplace while logged in, scraping a social platform's internal API with session cookies, mass-messaging from one account, automating thousands of actions per day on a single account.

Risks:

- Platforms detect repetitive/non-human action patterns (request frequency, identical timing, no idle gaps) — proxy quality alone does not protect the account.
- High volume from a single account triggers rate-limits and behavioral bans even when the IP looks clean.
- IP rotation across requests for a logged-in session is itself a strong signal (legitimate users do not change IP every 5 seconds) — do NOT rotate `sid` per request inside an account.

Required setup:

- Use Playbook A as the base (sticky `sid`, consistent geo, anti-detect browser, quality filter `medium` or `high`).
- Mobile proxies preferred over residential — higher trust, harder to ban.
- Throttle requests aggressively: add randomized delays (e.g. 3–15 seconds between actions), simulate idle gaps, avoid round-the-clock activity.
- Spread volume across multiple accounts, each with its own sub-user, sticky session, browser profile, and `sid`. Never push all volume through one account.
- Set realistic per-account daily quotas based on what a normal human would do on the platform (research the target's typical user behavior).
- Monitor `/statistics/requests/` per `proxy_username` — if request rate spikes beyond normal human patterns, throttle harder.

Required warning to communicate to the user:

> Scraping or high-volume automation inside a logged-in account carries real ban risk. Proxies and anti-detect browsers reduce IP/fingerprint detection, but platforms also detect behavior — request frequency, action patterns, missing idle time. Plan for: per-account daily quotas, randomized delays, and spreading load across multiple accounts. If the account is high-value, consider whether the workflow can be redesigned to use the platform's official API or to scrape public (logged-out) endpoints instead.

If the user is unsure whether their workflow falls into this category, the agent should ask:

- Are you logged into the account while doing this?
- Roughly how many requests/actions per hour per account?
- How valuable/established is the account (warmed up vs throwaway)?
- Is there a public/logged-out version of the same data?

---

## Tooling — proxy alone is not enough

```text
proxy + browser environment + automation tool = working setup
```

### For account workflows

Recommend an anti-detect browser. Platforms detect users by IP, fingerprint, device, cookies, storage, behavior, and geo mismatch — not just IP.

Recommended: **Multilogin**. Other anti-detect browsers also work.

Rules to communicate to the user:

- Use proxy + anti-detect browser together.
- Keep fingerprint and proxy geo consistent (timezone, language, locale).
- Do not mix different countries for the same account.
- Use separate browser profiles for separate accounts.
- Use sticky sessions for long account workflows.

### For scraping

Use Playwright, Puppeteer, Selenium, custom HTTP clients, or internal scraping pipelines. Anti-detect browsers are usually not required for simple scraping.

---

## Proxy gateway — how proxy traffic actually flows

Proxy traffic does NOT go through the API. It goes through the gateway:

```text
Host: gate.nodemaven.com
HTTP:    port 8080   (use this by default)
HTTPS:   port 9443   (use only if the user's tool requires HTTPS-tunnel proxy)
SOCKS5:  port 1080   (use when the tool/protocol requires SOCKS5)
```

### Proxy username format (CRITICAL — do not invent)

NodeMaven encodes targeting INSIDE the proxy username. The format is:

```text
<email_with_underscores>-country-<code>-region-<code>-city-<code>-isp-<code>-sid-<session_id>-filter-<level>
```

Rules:

- `email_with_underscores`: the user's NodeMaven account email with `@` and `.` replaced by `_`.
  Example: `firstname.lastname@example.com` → `firstname_lastname_example_com`.
  This base username is also returned by `GET /api/v2/base/users/me` as `proxy_username` — **always prefer the API value over reconstructing it from email.**
- `country`, `region`, `city`, `isp`: lowercase codes returned by `/locations/*` endpoints. **Resolve via API — never invent.**
- `sid` (session id): any string. Same `sid` = same exit IP for the duration of the sticky TTL. Use a unique `sid` per parallel session/account. Generate as random lowercase alphanumeric, 10–16 chars (e.g. via `openssl rand -hex 6`).
- `filter`: quality filter level. Allowed values: `medium`, `high`. Use `medium` by default; `high` for trust-sensitive workflows (ad accounts, marketplaces).
- Optional segments can be omitted, but order matters: country → region → city → isp → sid → filter.

Format example with placeholders (do not copy values literally — substitute the user's actual `proxy_username`, `proxy_password`, and resolved geo codes):

```text
Username: <proxy_username>-country-<COUNTRY_CODE>-region-<REGION_CODE>-isp-<ISP_CODE>-sid-<000000000000000>-filter-medium
Password: <proxy_password>
Host:     gate.nodemaven.com
Port:     <port>  (8080 for HTTP, 9443 for HTTPS, 1080 for SOCKS5)

Full proxy URL template:
http://<proxy_username>-country-<COUNTRY_CODE>-region-<REGION_CODE>-isp-<ISP_CODE>-sid-<000000000000000>-filter-medium:<proxy_password>@gate.nodemaven.com:<port>
```

### Concrete example (mock values for illustration only — do NOT use these in production)

This shows what the assembled URL looks like when every placeholder above is filled in. Values below are fictional — substitute the real ones returned by `/users/me` and `/locations/*`.

```text
proxy_username:  mock_user_example_com
proxy_password:  MOCK_PASSWORD_DO_NOT_USE
country code:    us
region code:     california
isp code:        spectrum
sid:             a1b2c3d4e5f6
filter:          medium
host:            gate.nodemaven.com
port:            8080  (HTTP)

Assembled username:
mock_user_example_com-country-us-region-california-isp-spectrum-sid-a1b2c3d4e5f6-filter-medium

Assembled full proxy URL:
http://mock_user_example_com-country-us-region-california-isp-spectrum-sid-a1b2c3d4e5f6-filter-medium:MOCK_PASSWORD_DO_NOT_USE@gate.nodemaven.com:8080
```

For SOCKS5, swap scheme and port. Format:

```text
socks5://<proxy_username>:<proxy_password>@gate.nodemaven.com:1080
```

Concrete SOCKS5 example with mock values:

```text
socks5://mock_user_example_com-country-us-sid-a1b2c3d4e5f6-filter-medium:MOCK_PASSWORD_DO_NOT_USE@gate.nodemaven.com:1080
```

### When to use sticky vs rotating

- **Sticky session** (account workflows): keep `sid` constant across all requests for that account. The same exit IP is held until the TTL expires. Default sticky TTL is controlled server-side; for long sessions plan to refresh or extend explicitly.
- **Rotating** (scraping): change `sid` per request (or omit it) to get a new exit IP each time.

### Whitelist-based access (no username/password)

If the user's automation runs from a fixed server IP, configure a whitelist instead. Allocated ports are returned by the whitelist API. Connect to `gate.nodemaven.com:<allocated_port>` from the whitelisted IP — no auth needed.

---

## End-to-end happy path (copy this pattern)

This is the minimum sequence the agent should run after receiving an API key. Every other API section in this skill is a deeper reference for these steps.

```bash
# 1. Validate API key and fetch base proxy credentials
curl -H "Authorization: x-api-key $API_KEY" \
  https://api.nodemaven.com/api/v2/base/users/me
# → returns: { "proxy_username": "...", "proxy_password": "...",
#             "email": "...", "traffic_limit": <bytes>,
#             "subscription_status": "...", "is_traffic_frozen": false }

# 2. Resolve country code (e.g. user said "USA")
curl -H "Authorization: x-api-key $API_KEY" \
  "https://api.nodemaven.com/api/v2/base/locations/countries/?limit=100&offset=0&name=United%20States&connection_type=residential"
# → use the returned "code" field (e.g. "us")

# 3. Resolve region (recommended for account workflows)
curl -H "Authorization: x-api-key $API_KEY" \
  "https://api.nodemaven.com/api/v2/base/locations/regions/?limit=100&offset=0&country__code=us&name=California&connection_type=residential"
# → use the returned "code" (e.g. "california")

# 4. Build the proxy URL using the format above:
#    http://<proxy_username>-country-us-region-california-sid-<000000000000000>-filter-medium:<proxy_password>@gate.nodemaven.com:<port>

# 5. Test the proxy
curl -x "http://<proxy_username>:<proxy_password>@gate.nodemaven.com:<port>" https://api.ipify.org
# substitute <port> with 8080 (HTTP), 9443 (HTTPS), or 1080 (SOCKS5 — also change scheme to socks5://)
# → returns a US/California IP

# 6. Monitor traffic after the user starts using the proxy
curl -H "Authorization: x-api-key $API_KEY" \
  "https://api.nodemaven.com/api/v2/base/statistics/data/?proxy_username=<proxy_username>&period=hours24&request_source=proxy"
```

Concrete example of what step 4 produces (mock values — for illustration only):

```bash
# After /users/me returned proxy_username=mock_user_example_com, proxy_password=MOCK_PASSWORD_DO_NOT_USE
# After /locations/countries returned code=us
# After /locations/regions returned code=california
# Generated sid=a1b2c3d4e5f6, chose filter=medium, port=8080 (HTTP)

curl -x "http://mock_user_example_com-country-us-region-california-sid-a1b2c3d4e5f6-filter-medium:MOCK_PASSWORD_DO_NOT_USE@gate.nodemaven.com:8080" \
  https://api.ipify.org
# → returns a California IP
```

If any step fails, fall back to the relevant section below.

---

# API reference

All endpoints below are relative to `https://api.nodemaven.com` and require the `Authorization: x-api-key <KEY>` header.

## 1. Validate user / get proxy credentials

```http
GET /api/v2/base/users/me
```

Returns at minimum:

```json
{
  "email": "user@example.com",
  "proxy_username": "user_example_com",
  "proxy_password": "<proxy_password>",
  "traffic_limit": 53687091200,
  "traffic_used": 1073741824,
  "subscription_status": "active",
  "is_traffic_frozen": false
}
```

Agent behavior:

- If the request fails with 401/403, the API key is wrong or revoked → ask user to re-copy from the API Key page link.
- If `is_traffic_frozen: true` or `traffic_used >= traffic_limit` → send the user to the Subscriptions or PAG link.
- Use `proxy_username` and `proxy_password` to build proxy URLs (unless using whitelist).
- Use `proxy_username` for all `/statistics/*` queries.

---

## 2. Connection type and IPv4 filtering

For all `/locations/*` endpoints:

```text
connection_type=residential   # default, use for most workflows
connection_type=mobile        # smaller pool, higher trust, account workflows
ipv4_only=true                # only locations that have IPv4-capable IPs
ipv4_only=false               # default behavior
```

Use `ipv4_only=true` only when the user's target site is known to be IPv6-incompatible (rare). Otherwise leave it off.

---

## 3. Resolve location targeting

The agent must NEVER invent country, region, city, ISP, or ZIP codes. Resolve in order:

```text
country → region → city → ISP / ZIP
```

Use returned `code` values (lowercase) in proxy username and whitelist body.

### 3.1 Full location reference (rarely needed)

```http
GET /api/v2/base/locations/all-doc/
```

Use only if the agent needs to inspect the full location model. For normal flow, use the specific endpoints below.

### 3.2 Countries

```http
GET /api/v2/base/locations/countries/
```

Parameters: `limit`, `offset`, `name`, `code`, `connection_type`, `ipv4_only`.

Examples:

```http
GET /api/v2/base/locations/countries/?limit=100&offset=0&connection_type=residential
GET /api/v2/base/locations/countries/?limit=100&offset=0&name=United States&connection_type=residential
GET /api/v2/base/locations/countries/?limit=100&offset=0&code=us&connection_type=residential
```

If the user says "USA", "America", "the States" — resolve to `us`. If unsure, query by `name=` first.

### 3.3 Regions

```http
GET /api/v2/base/locations/regions/
```

Parameters: `limit`, `offset`, `country__code` (required), `name`, `code`, `connection_type`, `ipv4_only`.

```http
GET /api/v2/base/locations/regions/?limit=100&offset=0&country__code=us&connection_type=residential
GET /api/v2/base/locations/regions/?limit=100&offset=0&country__code=us&name=California&connection_type=residential
```

For account management, region targeting is strongly recommended.

### 3.4 Cities

```http
GET /api/v2/base/locations/cities/
```

Parameters: `limit`, `offset`, `country__code`, `region__code`, `name`, `code`, `connection_type`, `ipv4_only`.

```http
GET /api/v2/base/locations/cities/?limit=100&offset=0&country__code=us&region__code=california&connection_type=residential
GET /api/v2/base/locations/cities/?limit=100&offset=0&country__code=us&region__code=california&name=Los Angeles&connection_type=residential
```

Use city targeting for high-risk account workflows, local SERP checks, ad verification, marketplace automation.

### 3.5 ISP provider targeting

ISP here means provider targeting **inside** residential/mobile rotating proxies. It is not a separate proxy product.

```http
GET /api/v2/base/locations/isps/
```

Required: `limit`, `offset`, `country__code`. Optional: `region__code`, `city__code`, `name`, `code`, `connection_type`, `ipv4_only`.

```http
GET /api/v2/base/locations/isps/?limit=100&offset=0&country__code=us&region__code=california&connection_type=residential
GET /api/v2/base/locations/isps/?limit=100&offset=0&country__code=us&name=Spectrum&connection_type=residential
```

Use ISP targeting for ad accounts, marketplaces, and any workflow where network reputation matters.

Helper endpoints (use when the user asks where ISP targeting is available):

```http
GET /api/v2/base/locations/isps/regions/?country__code=us&connection_type=residential
GET /api/v2/base/locations/isps/cities/?country__code=us&region__code=california&connection_type=residential
```

### 3.6 ZIP targeting

Use ZIP only when local precision is required (local SERP, ads verification, local marketplace testing). Some ZIPs in the list may be unavailable.

```http
GET /api/v2/base/locations/zipcodes/?limit=100&offset=0&country__code=us&region__code=california&city__code=los-angeles&connection_type=residential
GET /api/v2/base/locations/zipcodes/?limit=100&offset=0&country__code=us&zip=90001&connection_type=residential
```

Helper endpoints:

```http
GET /api/v2/base/locations/zipcodes/regions/?country__code=us&connection_type=residential
GET /api/v2/base/locations/zipcodes/cities/?country__code=us&region__code=california&connection_type=residential
```

For account management, city or ISP is usually enough — do not default to ZIP.

---

## 4. Whitelist (IP-auth access for fixed servers)

Use whitelist when the user runs automation from a fixed IP (VPS, cloud server, office network, scraping server, backend service). Whitelist allocates proxy ports for a trusted source IP — no username/password needed.

Do NOT use whitelist when:

- The user's IP changes often.
- The user only needs username/password proxy auth from a laptop.

### 4.1 List whitelisted IPs

```http
GET /api/v2/base/whitelist/ips?page=1&page_size=10
```

Response includes `id`, `ports`, `country_code`, `region_code`, `city_code`, `isp_code`, `ip`, `name`, `ttl`, `protocol`, `quality_filter_enabled`, `number_of_proxies`, `sticky`, `is_duplicated`, `created`, `updated`.

Always check existing entries before creating a new one.

### 4.2 Create or update whitelist IP

```http
POST /api/v2/base/whitelist/ip/upsert
```

Required: `ip`, `ports_count`. Optional: `id` (for update), `name`, `sticky`, `ttl`, `protocol`, `quality_filter_enabled`, `country`, `region`, `city`, `isp`.

Account workflow body (template):

```json
{
  "ip": "<SERVER_IP>",
  "name": "Account Automation",
  "sticky": true,
  "ttl": 3600,
  "protocol": "HTTP",
  "quality_filter_enabled": true,
  "ports_count": 5,
  "country": "<COUNTRY_CODE>",
  "region": "<REGION_CODE>",
  "city": "<CITY_CODE>",
  "isp": "<ISP_CODE>"
}
```

All `<*_CODE>` values must come from the matching `/locations/*` endpoint. Do not hardcode them.

Concrete example (mock values for illustration only — substitute the user's real server IP and API-resolved location codes):

```json
{
  "ip": "203.0.113.42",
  "name": "Account Automation",
  "sticky": true,
  "ttl": 3600,
  "protocol": "HTTP",
  "quality_filter_enabled": true,
  "ports_count": 5,
  "country": "us",
  "region": "california",
  "city": "los-angeles",
  "isp": "spectrum"
}
```

Scraping body (template):

```json
{
  "ip": "<SERVER_IP>",
  "name": "Scraping Server",
  "sticky": false,
  "ttl": 3600,
  "protocol": "HTTP",
  "quality_filter_enabled": false,
  "ports_count": 20,
  "country": "<COUNTRY_CODE>"
}
```

Concrete example (mock values):

```json
{
  "ip": "198.51.100.17",
  "name": "Scraping Server",
  "sticky": false,
  "ttl": 3600,
  "protocol": "HTTP",
  "quality_filter_enabled": false,
  "ports_count": 20,
  "country": "us"
}
```

Field semantics:

```text
ip                       source IP allowed to use the proxy (no auth needed from this IP)
name                     human label
sticky                   true = same exit IP per port, false = rotate per request
ttl                      sticky session lifetime in seconds (3600 = 1h, 86400 = 24h)
protocol                 HTTP or SOCKS5
quality_filter_enabled   true = lower fraud-score IPs (recommended for accounts)
ports_count              number of allocated ports — match expected parallelism
country/region/city/isp  lowercase codes from /locations/* endpoints
```

Defaults to recommend:

- Account: `sticky: true`, `quality_filter_enabled: true`, `ttl: 3600` (or longer for very long sessions), country + region minimum.
- Scraping: `sticky: false`, `quality_filter_enabled: false`, country only.
- `ports_count`: 5 for accounts, 10–20 for scraping. Tune to expected concurrency.

### 4.3 Get / delete whitelist by ID

```http
GET    /api/v2/base/whitelist/ip/{id}
DELETE /api/v2/base/whitelist/ip/{id}
```

Always confirm with the user before deleting.

---

## 5. Sub-users (isolation)

Use sub-users to isolate workflows: multiple accounts, multiple clients, separate scraping jobs, team access, traffic limits per workflow, separating test from production.

Each sub-user has its own `proxy_username` / `proxy_password`.

### 5.1 List

```http
GET /api/v2/base/sub-users/?page=1&per_page=20
GET /api/v2/base/sub-users/?id=<SUB_USER_ID>
```

Always check existing sub-users before creating.

### 5.2 Create

```http
POST /api/v2/base/sub-users/
```

Template:

```json
{
  "proxy_username": "<sub_user_name>",
  "proxy_password": "<proxy_password>",
  "is_traffic_limited": true,
  "traffic_limit": <bytes>
}
```

Concrete example (mock values):

```json
{
  "proxy_username": "client_account_1",
  "proxy_password": "MOCK_PASSWORD_DO_NOT_USE_v1",
  "is_traffic_limited": true,
  "traffic_limit": 10737418240
}
```

Generate `proxy_password` with a strong random generator (e.g. `openssl rand -base64 24 | tr -d '=+/' | cut -c1-20`). Do not copy the example password above into real requests.

Validation rules:

```text
proxy_username: 9–100 chars, [a-zA-Z0-9_] only
proxy_password: 9–100 chars, [a-zA-Z0-9_] only
traffic_limit:  bytes
```

If the user provides names with `-`, spaces, or non-ASCII, sanitize them: replace with `_`, then verify length ≥ 9. Ask the user to confirm the sanitized name.

Traffic limit conversions:

```text
1 GB  = 1073741824
10 GB = 10737418240
50 GB = 53687091200
```

### 5.3 Update

```http
PUT /api/v2/base/sub-users/
```

Template:

```json
{
  "id": "<sub_user_id>",
  "proxy_username": "<sub_user_name>",
  "proxy_password": "<proxy_password>",
  "is_traffic_limited": true,
  "traffic_limit": <bytes>
}
```

Concrete example (mock values):

```json
{
  "id": "MOCK_SUB_USER_ID_DO_NOT_USE",
  "proxy_username": "client_account_1",
  "proxy_password": "MOCK_PASSWORD_DO_NOT_USE_v2",
  "is_traffic_limited": true,
  "traffic_limit": 21474836480
}
```

Or increment instead of setting:

```json
{ "id": "<sub_user_id>", "traffic_limit_increment_bytes": 10737418240 }
```

`traffic_limit_increment_bytes` is mutually exclusive with `traffic_limit`. Negative values subtract.

### 5.4 Delete / reset usage

```http
DELETE /api/v2/base/sub-users/?id=<SUB_USER_ID>
POST   /api/v2/base/sub-users/reset/usage
```

Reset body:

```json
{ "ids": ["<SUB_USER_ID_1>", "<SUB_USER_ID_2>"] }
```

The default (root) user's usage cannot be reset.

---

## 6. Statistics

All statistics endpoints require `proxy_username`. Optional: `timezone`, `start`, `end` (date format `dd-mm-yyyy`), `period` (`today` | `hours24`), `request_source` (`proxy` | `browser`).

`request_source=proxy` covers all traffic via gateway (curl, Playwright, anti-detect, etc.). Use `browser` only if NodeMaven exposes browser-side telemetry separately and the user explicitly asks for it; otherwise default to `proxy`.

### 6.1 Traffic usage

```http
GET /api/v2/base/statistics/data/?proxy_username=<USERNAME>&period=hours24&request_source=proxy
```

Returns `{ "labels": [...], "data": [...] }` where `data` is bytes per bucket.

### 6.2 Requests

```http
GET /api/v2/base/statistics/requests/?proxy_username=<USERNAME>&period=hours24&request_source=proxy
```

`data` is request count per bucket. Use to confirm traffic is actually flowing or debug zero-request cases.

### 6.3 Domains

```http
GET /api/v2/base/statistics/domains/?proxy_username=<USERNAME>&limit=20&period=hours24&request_source=proxy
```

Use to see which domains consume traffic — useful for catching unexpected destinations or traffic leaks.

---

## 7. Notifications

```http
GET    /api/v2/base/notifications/
DELETE /api/v2/base/notifications/{notification_id}
```

Check unread notifications when:

- The user reports an issue.
- Before starting a large workflow.
- Debugging unexpected account state.

Only mark as read after the user confirms or after the issue is handled.

---

# Playbooks

## Playbook A — Account management

Use when the user manages social, marketplace, freelance, marketing, or e-commerce accounts.

Ask the user (in one message):

- What platform are you working with?
- How many accounts do you manage?
- Where were the accounts created and last used?
- Are accounts new or warmed up?
- Short actions or long sessions?
- Are you using an anti-detect browser?
- Running locally or from a server?

Recommendation:

- Residential or mobile proxies (mobile for higher-trust workflows)
- Country + region minimum; city or ISP if needed
- `sticky: true`, `quality_filter_enabled: true`
- `filter=medium` by default, `filter=high` for ad/marketplace accounts
- Anti-detect browser (Multilogin or equivalent)
- Separate browser profile per account
- Sub-user per account group if multi-client

API sequence:

1. `GET /api/v2/base/users/me` — validate, get base credentials
2. `GET /api/v2/base/locations/countries/?...&connection_type=residential` — resolve country
3. `GET /api/v2/base/locations/regions/?country__code=<X>&...` — resolve region
4. (optional) `GET /api/v2/base/locations/cities/?...` — resolve city
5. (optional) `GET /api/v2/base/locations/isps/?...` — resolve ISP
6. (optional) `POST /api/v2/base/sub-users/` — isolate account groups
7. (server-based) `POST /api/v2/base/whitelist/ip/upsert` with sticky body above
8. Build proxy URL (laptop) OR use allocated whitelist port (server)
9. Plug proxy into anti-detect browser profile
10. `GET /api/v2/base/statistics/data/` and `/requests/` for monitoring

Hard rules to communicate:

- Keep account geo, proxy geo, timezone, language, and browser fingerprint consistent.
- Do not rotate across countries.
- Do not reuse one browser profile for many accounts.
- Use a unique `sid` per account; keep it constant for that account.

## Playbook B — Scraping

Use when the user collects public data at scale.

Ask the user:

- What site?
- Source country?
- Browser rendering needed?
- How many pages/requests?
- Public or logged-in?
- Local or server?
- Concurrent sessions?

Recommendation:

- Residential rotating
- `sticky: false`, `quality_filter_enabled: false` (unless target is sensitive)
- Country only unless local results are required
- Larger `ports_count` for parallelism
- Playwright / Puppeteer / Selenium / custom HTTP client

API sequence:

1. `GET /api/v2/base/users/me`
2. `GET /api/v2/base/locations/countries/?...`
3. (optional) regions/cities for local targeting
4. (server) `POST /api/v2/base/whitelist/ip/upsert` with rotating body
5. Run scraping through `gate.nodemaven.com:<port>` (vary `sid` per request, or omit)
6. Monitor with `/statistics/data/`, `/requests/`, `/domains/`

Hard rules:

- Rotate IPs for scale (vary `sid`).
- Don't pin one IP for high-scale unless required.
- Country-only targeting by default.
- Watch top domains to catch leaks.

## Playbook C — Browser automation

Classify first:

- Account automation → Playbook A
- Data extraction (no login) → Playbook B
- Scraping or high-volume actions inside a logged-in account → Playbook A + the warnings in "Edge case: scraping or high-volume actions inside an account" above. Do NOT rotate `sid` per request. Throttle and spread load across multiple accounts.
- Fixed server → whitelist
- Multi-workflow → sub-users

Then follow the matched playbook.

---

# Agent decision rules

Always:

- Validate the API key before anything else.
- Ask the user's goal before recommending proxy type.
- Resolve geo codes via API; never invent them.
- Use country + region minimum for account workflows.
- Use sticky sessions with constant `sid` for account workflows.
- Use rotating sessions (varying `sid`) for scraping — but ONLY for logged-out / public scraping. Never rotate `sid` per request inside a logged-in account.
- For high-volume automation inside an account, warn the user explicitly about behavioral ban risk and recommend throttling + load-spreading across multiple accounts.
- Use `quality_filter_enabled: true` / `filter=medium` by default for accounts; `filter=high` for trust-sensitive.
- Use sub-users for isolation across clients/accounts.
- Use whitelist for fixed-server automation.
- Explain external tooling required (anti-detect browser for accounts, automation framework for scraping).
- Build the full proxy URL for the user — do not leave placeholders like `<HOST>` in the final answer.

Never:

- Invent country / region / city / ISP / ZIP codes.
- Invent the proxy username syntax — follow the format in this skill.
- Send `Authorization: Bearer ...` or a separate `x-api-key` header.
- Assume purchase or signup happens via API.
- Use random geo for accounts.
- Rotate accounts across countries.
- Recommend one fixed IP for high-scale scraping by default.
- Claim proxies alone are enough for account workflows.
- Strip UTM parameters from tracked links.
- Echo the full API key, proxy password, or full proxy URL back to the user unnecessarily — mask or use placeholders. See "Security and credential hygiene" above.
- Hardcode API keys or proxy passwords into code artifacts — use environment variables.
- Log or persist verbatim responses from `/users/me` or `/sub-users/` — they contain `proxy_password`.
- Copy literal example values from this skill (like `<YOUR_API_KEY>`, `<proxy_password>`, `<COUNTRY_CODE>`) into real API calls — they are placeholders.

---

# Minimal response templates

## User has no account

> To get started, create a NodeMaven account: https://dashboard.nodemaven.com/accounts/signup/?utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill — then pick a plan: subscription (https://dashboard.nodemaven.com/pricing?tab=MONTHLY_PLANS&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill) or Pay As You Go (https://dashboard.nodemaven.com/pricing?tab=PAG&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill). After purchase, grab your API key here: https://dashboard.nodemaven.com/user-profile?tab=API_KEY&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill — paste it back to me and I'll set everything up.

## User has account, not logged in

> Log in: https://dashboard.nodemaven.com/accounts/login/?utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill — then copy your API key from https://dashboard.nodemaven.com/user-profile?tab=API_KEY&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill and send it here so I can validate it and configure your setup.

## User wants account management

> For account workflows you need residential or mobile proxies with stable geo. Minimum setup: country + region, sticky sessions, quality filter `medium` (or `high` for ad/marketplace accounts). Pair this with an anti-detect browser like Multilogin — platforms detect both IP and browser fingerprint. Send me your API key and target country so I can build the exact proxy URL.

## User wants scraping

> For scraping use rotating residential proxies. Default: country-only targeting, sticky off, varying `sid` per request, larger port allocation. Pair with Playwright / Puppeteer / Selenium / a custom HTTP client. Send me your API key, target country, and concurrency so I can configure it.

## User provides API key

> Validating now. I'll call `GET /api/v2/base/users/me`, then resolve location codes, set up whitelist or sub-user if needed, and give you the exact proxy URL ready to paste into your tool.

---

# Summary

```text
user task → proxy recommendation → account/API setup → location resolution → access configuration → external tool setup → monitoring
```

API for: validation, location discovery, whitelist, sub-users, monitoring.
Gateway for: scraping, browser automation, anti-detect sessions, account workflows.

For full success, combine:

```text
correct proxy type + correct geo + correct session strategy (sticky/rotating + sid) + correct external tool
```

If anything is uncertain, the agent's defaults are: residential, country+region targeting, sticky for accounts / rotating for scraping, `filter=medium`, HTTP protocol (port 8080).
