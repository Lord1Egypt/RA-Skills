# Marketing copy (for skill marketplace listing)

---

## Short tagline

B2B company enrichment from public data. Guessed email patterns, scraped descriptions, optional LLM metadata.

## Long description

A basic B2B lead enrichment tool. Input company names, get back guessed domains, scraped homepage descriptions, email patterns, and social links.

**What v1.0 actually does:**
- Guesses company domains from names
- Scrapes public homepage content (HTTPS only, robots.txt-respecting)
- Generates email address patterns (guesses, not verified)
- Extracts social links from homepage
- Optional LLM description extraction (MINIMAX_API_KEY required)

**What's NOT in v1.0 (coming in v1.1):**
- Verified decision-maker names
- LinkedIn profile enrichment
- CRM import
- Personalized outreach draft generation
- Multi-lead bulk parallel processing

## Compliance & privacy

- Scrapes public data only — you are responsible for lawful use
- Do not send outreach to scraped addresses without verifying them first
- Comply with CAN-SPAM, GDPR, and local laws for your jurisdiction
- No personal data is collected or processed beyond public homepage content
- Do not provide LinkedIn session cookies — not used in v1.0

## License

MIT
