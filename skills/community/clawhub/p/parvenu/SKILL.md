---
name: parvenu
description: B2B lead lists with verified emails, work-email lookup, LinkedIn profile enrichment and company search via Parvenu.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PARVENU_API_KEY
      bins:
        - curl
    primaryEnv: PARVENU_API_KEY
    envVars:
      - name: PARVENU_API_KEY
        required: true
        description: Your Parvenu API key, from your account at app.parvenu.io. Every call is billed to this account's credits.
    emoji: "🎯"
    homepage: https://parvenu.io
---

# Parvenu: B2B lead sourcing and enrichment

Parvenu finds B2B contacts and companies and enriches them with verified emails,
LinkedIn data and company facts. This skill calls the Parvenu API at
`https://api.parvenu.io` with the user's `PARVENU_API_KEY`.

## Costs (tell the user before spending)

Parvenu bills in credits on the user's own account. Say the likely cost before any
billed call, and confirm before anything over ~50 credits.

| Action | Endpoint | Cost |
|---|---|---|
| Credit balance | `/credit_check` | Free |
| Your lists | `/all_list` | Free |
| Lead list with verified emails | `/lead_enrichment_list` | 1 credit per valid email (0.2 per record with `email_enrichment: false`) |
| One person's email | `/email_enrichment` | 1 credit when found, misses free |
| One LinkedIn profile | `/profile` | 1 credit |
| Company search | `/company_search` | 0.2 credits per company returned |

## How to call the API

Every call is a JSON `POST` with the key in the body. Always use the helper: it
adds the key from `PARVENU_API_KEY` without putting it on a command line, and it
exits non-zero (printing the API's error) when a call fails:

```bash
{baseDir}/scripts/parvenu.sh /credit_check '{}'
```

The helper only accepts the endpoints listed in this skill. The body must be a
JSON object; it may span several lines.

Never echo, log or paste the key into the chat. If `PARVENU_API_KEY` is missing,
tell the user to set it; do not ask them to paste it into the conversation.

## Workflows

### 1. Build a lead list (async)

1. Start the job:

   ```bash
   {baseDir}/scripts/parvenu.sh /lead_enrichment_list '{
     "listname": "Roofing owners California",
     "fetch_count": 50,
     "contact_job_title": ["Owner", "CEO", "Founder"],
     "company_keywords": ["roofing"],
     "contact_location": ["california, us"],
     "size": ["11-50"],
     "email_enrichment": true
   }'
   ```

   Filters (all optional, all arrays): `contact_job_title`, `contact_not_job_title`,
   `company_keywords`, `company_not_keywords`, `company_industry`,
   `company_not_industry`, `company_domain`, `contact_location`,
   `contact_not_location`, `contact_city`, `size`.
   - `contact_location` is `"state, country_code"` with the state spelled out
     (`"texas, us"`, never `"TX"`), or a full country name. Check a value with
     `/search_lead_locations` and `{"search": "texas"}` (free).
   - `size` buckets: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`,
     `1001-5000`, `5001-10000`, `10001+`.
   - `unique` defaults to `true`: people already in the account are skipped and not
     charged, so the list can come back smaller than `fetch_count`.
2. Poll until done (free), every 20–30 seconds:

   ```bash
   {baseDir}/scripts/parvenu.sh /check_list_status '{"listname": "Roofing owners California"}'
   ```
3. Download the rows (500 per page, use `offset` for the next page):

   ```bash
   {baseDir}/scripts/parvenu.sh /download_list '{"listname": "Roofing owners California", "limit": 500, "offset": 0}'
   ```

### 2. Find one person's work email

Send the LinkedIn URL when you have it; otherwise name plus company or domain.

```bash
{baseDir}/scripts/parvenu.sh /email_enrichment '{"person_linkedin_url": "https://www.linkedin.com/in/example"}'
{baseDir}/scripts/parvenu.sh /email_enrichment '{"name": "Jane Doe", "domain": "acme.com"}'
```

Returns the work email first; if none, a verified personal email. Never a shared
inbox like info@.

### 3. Enrich a LinkedIn profile

```bash
{baseDir}/scripts/parvenu.sh /profile '{"person_linkedin_url": "https://www.linkedin.com/in/example"}'
```

### 4. Search companies

```bash
{baseDir}/scripts/parvenu.sh /company_search '{
  "ai_keywords": ["cybersecurity"],
  "country_codes": ["us"],
  "employee_buckets": ["51-200"],
  "page": 1,
  "page_size": 25
}'
```

Results are paged; ask before pulling more pages, since each company costs 0.2
credits.

### 5. Account

- Balance: `/credit_check` with `{}`.
- Lists on the account: `/all_list` with `{}`.

## Going further

Parvenu has 100+ more actions (company news, tech stack, hiring managers, ICP
scoring, Google Maps leads, LinkedIn post engagers, AI research per row). The full
reference is at https://developer.parvenu.io.

For MCP clients, the same capabilities are available as a remote MCP server at
`https://enterprise.parvenu.io/mcp` (streamable HTTP).

## Rules

- Never invent emails, phone numbers or company facts; only report what the API returns.
- Confirm before large or repeated billed calls, and report credits used after.
- Respect the rate limit: at most 5 requests per second per key. Poll async jobs no
  faster than every 20 seconds.
