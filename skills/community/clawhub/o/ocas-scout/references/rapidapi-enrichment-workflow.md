# RapidAPI Enrichment Workflow

> **When to invoke:** During Phase 3 (Handle Expansion) and Phase 4 (Email/Phone Tools) of the research workflow. Use RapidAPI social media endpoints to enrich profiles with structured data that free tools (Sherlock/Maigret) can't provide.

## Person Enrichment Pipeline

When a known handle/username is found for a subject, query these RapidAPI endpoints **in parallel**:

### Twitter/X Enrichment

```
rapidapi_call("twitter154", "User_Details", {"username": handle})
```

Returns: user_id, name, follower/following count, tweet count, creation date, profile info.

If write access needed (e.g., fetching full timeline):

```
rapidapi_call("twitter-api47", "Create_Post_Quote", {...})  # 63 tools including write ops
```

**LinkedIn Note (June 1 2026):** 5 OLD LinkedIn APIs are non-functional. They return "We are no longer providing this service" or "Service Unavailable." Do NOT use them.

✅ **NEW working API:** `fresh-linkedin-scraper-api.p.rapidapi.com` — 43 tools. Works for person profiles, company profiles, search, education, skills, experiences, contact info.

### LinkedIn Enrichment (person)

```
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Profile", {"username": handle})
```

Returns: full_name, headline, location, summary, is_premium, is_open_to_work, is_hiring.

Then get URN from response and use for detailed queries:

```
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Experiences", {"username": handle, "urn": urn})
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Educations", {"username": handle, "urn": urn})
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Skills", {"username": handle, "urn": urn})
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Contact", {"username": handle})
rapidapi_call("fresh-linkedin-scraper-api", "Get_User_Follower_And_Connection", {"username": handle})
```

Search:

```
rapidapi_call("fresh-linkedin-scraper-api", "Search_People", {"name": "First Last", "limit": 5})
```

### LinkedIn Enrichment (company)

```
rapidapi_call("fresh-linkedin-scraper-api", "Get_Company_Profile", {"company_id": id})
rapidapi_call("fresh-linkedin-scraper-api", "Search_People", {"keyword": company_name, "filters": {"current_company": [company_id]}})
```

### Instagram Enrichment

```
rapidapi_call("instagram-looter2", "Web_profile_info_by_username", {"username": handle})
rapidapi_call("instagram-scraper-stable-api", "Account_Data_V2", {"username_or_url": handle})
rapidapi_call("flashapi1", "User_Info_by__username", {"username": handle})
```

Returns: bio, follower/following count, profile pic URL, is_private, is_verified, media count.

If Instagram returns user ID, fetch posts:

```
rapidapi_call("instagram-looter2", "Media_list_by_user_ID", {"user_id": id, "limit": 10})
```

### Facebook Enrichment

```
rapidapi_call("facebook-scraper3", "Search_place", {"query": name})
rapidapi_call("facebook-scraper3", "Listing_details", {"id": place_id})
```

### People Search / Skip Tracing

```
rapidapi_call("skip-tracing-working-api", "__trace_by_email", {"email": email})
rapidapi_call("skip-tracing-working-api", "_trace_by_address", {"address": address})
rapidapi_call("email-finder7", "Find_Email", {"domain": domain, "first_name": name, "last_name": name})
rapidapi_call("viewcaller", "Search_Contact", {"phone": phone})
rapidapi_call("truecaller-data2", "Search", {"phone": phone})
rapidapi_call("whoisapi", "whois_lookup_v1", {"domain": domain})
```

### Contact Enrichment (from email/phone)

```
rapidapi_call("phoneinfoga", "scan", {"phone": phone})  # if available locally
rapidapi_call("email-finder7", "Find_By_Domain", {"domain": domain})
```

## Company Enrichment Pipeline

When researching a company/organization:

```
rapidapi_call("linkedin-api-search", "search", {"keyword": company_name, "filters": {"location_us": [...]}})
rapidapi_call("linkedin-api-data", "companyDetail", {"id": company_id})
rapidapi_call("similarweb-insights", "Website_Details", {"domain": company_domain})
rapidapi_call("similarweb-insights", "Similar_Sites", {"domain": company_domain})
rapidapi_call("indeed-jobs", "search", {"query": company_name, "location": ""})
rapidapi_call("active-jobs-db", "Ultra_-_Get_Modified_Jobs_24h", {"search": company_name})
```

Returns: company size, industry, web traffic, similar companies, recent job postings.

## Data Extraction & Provenance

For every RapidAPI call that returns data:
1. Record the source URL/handle in the source log
2. Extract key entities (name, title, location, company, email, phone)
3. Assign confidence based on data richness:
   - **high:** 3+ data points match (name + title + company, or name + location + handle)
   - **medium:** 2 data points match
   - **low:** 1 data point or username-only match
4. Emit Signal to Elephas for confirmed entities
5. Include RapidAPI source reference in the brief's Source Log

## Rate Limiting & Error Handling

- All RapidAPI calls use the shared MCP broker at `https://mcp.rapidapi.com`
- If an API returns "not subscribed" or "quota exceeded", skip and try the next variant
- Twitter: try twitter154 first, fall back to twitter/twitter-x-api
- Instagram: try instagram-looter2 first, fall back to instagram-scraper-stable-api / flashapi1
- LinkedIn: fresh-linkedin-scraper-api (primary) → linkedinscraper → linkedin-email-finder5 → linkedin-lead-enrichment. 5 old APIs non-functional.
- Never block the research pipeline on a single API failure

## Integration with Existing Tiers

- **Tier 1 (free tools):** theHarvester, Sherlock, Maigret, OpenSanctions — run first
- **RapidAPI Enrichment:** run in parallel with Tier 1 tools when handles/emails/phones are known
- **Tier 2 (extended):** Run if RapidAPI enrichment is insufficient
- **Tier 3 (paid):** Requires explicit permission, same as before

RapidAPI enrichment replaces the need for some Tier 2 sources (e.g., Social Analyzer for basic username checks) but does not replace specialized OSINT tools (Holehe, h8mail, PhoneInfoga, Ghunt).

## Reference

Full API rankings, tool names, and param patterns: `~/.hermes/references/rapidapi/`
