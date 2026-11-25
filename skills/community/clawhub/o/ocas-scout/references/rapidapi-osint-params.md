# RapidAPI — OSINT Enrichment Quick Reference

> For use by ocas-scout during Phase 3/4 enrichment. All endpoints verified working June 2026.

## Working Endpoints & Correct Params

### Instagram (primary: instagram-looter2)
- Web_profile_info_by_username: {"username": "handle"} → followers, bio, is_private, is_verified, posts_count
- User_info_V2_by_username: {"username": "handle"} → enhanced profile
- Media_list_by_user_ID: {"user_id": "numeric_id", "limit": 10} → posts (need user_id first)

### Twitter (primary: twitter154)
- User_Details: {"username": "handle"} → follower/following count, tweet count, created_at, location
- Search: {"query": "@handle", "limit": 5} → tweets

### LinkedIn (primary: linkedin-bulk-data-scraper)
- person_data_with_educations: {"linkedin_url": "https://www.linkedin.com/in/HANDLE"} → full profile
- NOTE: linkedin-api-data disabled ("no longer providing this service")

### Skip Tracing (skip-tracing-working-api)
- __trace_by_name: {"name": "First Last"} → nationwide (filter client-side)
- __trace_by_email: {"email": "user@domain.com"} → person records
- __trace_by_name_and_address: {"name": "First Last", "city": "City", "state": "ST"} → targeted
- NOTE: Many false positives — always filter by age/location

### Email Finding (email-finder7)
- Find_Email: {"first_name": "First", "last_name": "Last", "domain": "company.com"}
- Find_By_Domain: {"domain": "company.com"} → up to 5 emails

### WHOIS (whoisapi)
- whois_lookup_v1: {"domainName": "example.com"} — param is camelCase domainName

### IP Reputation (netdetective)
- query: {"ip": "X.X.X.X"} → VPN/datacenter/brute_force/spam flags

### Reverse Image (reverse-image-search-by-copyseeker)
- Scan_image: {"image_url": "https://..."} → needs publicly accessible URL

### Web Scraping (scrapeninja)
- scrape: {"url": "https://..."} → JS-rendered page content

## NOT Subscribed
- people-data-lookup.p.rapidapi.com
- phone-social-data-enrichment.p.rapidapi.com
- social-media-scanner1.p.rapidapi.com (rate limited)
- osint5.p.rapidapi.com (returns Google page, not OSINT)

## Fallback Order
- Instagram: instagram-looter2 → instagram-scraper-stable-api → flashapi1 → instagram28
- Twitter: twitter154 → twitter135 → twitter-aio → twitter-x-api
- LinkedIn: linkedin-bulk-data-scraper → linkedin-api8 → linkedin-api-data (disabled)
- People search: skip-tracing-working-api → email-finder7
- Reverse image: reverse-image-search-by-copyseeker → real-time-image-search