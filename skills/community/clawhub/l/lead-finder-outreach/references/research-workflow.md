# Research Workflow

Use public sources only. The goal is to build a defensible 50-company shortlist, not a contact-enrichment database.

## Source Priority

### Tier 1: Primary public evidence

- Official company website
- Service pages
- Location pages
- About pages
- Contact pages
- Booking or appointment pages

### Tier 2: Public directories and profiles

- Google Business style profiles
- Public local directories
- Industry directories
- Public company social profiles

### Tier 3: Lightweight corroboration

- Press releases
- Local chamber or association pages
- Public portfolio pages

## Workflow

1. Parse the request into search constraints: niche, geography, fit criteria, count, and any exclusion rules.
1. Build seed queries from the niche, the location, and likely business variants.
1. Search for candidate companies using public sources only.
1. Open each candidate's website or profile and confirm it is a real business in the requested market.
1. Confirm at least one usable public contact path, such as:
   - contact page
   - appointment page
   - booking page
   - consultation page
1. Capture the key public fields for each company.
1. Rank candidates by relevance to the request and contact-path quality.
1. Keep searching until 50 qualified companies are validated or the public evidence pool is exhausted.

## Qualification Rules

Include a company only if all of these are true:

- It is a real business that matches the requested niche.
- The evidence is public and directly reachable by URL.
- It has a public website.
- The fit is explainable in one sentence without speculation.

Exclude a company if any of these are true:

- It is a directory result, aggregator page, or third-party profile without a usable business website.
- Its business type is unrelated to the requested niche.
- The proof depends on private data, scraping, or inferred contact intelligence.
- The source pages are too thin to justify a prospecting recommendation.

## Ranking Heuristics

Prefer companies with:

- Clear niche match
- Strong geography match
- Same-site contact or booking paths
- Visible business details on the official website
- Geography match if location matters
- Stronger direct contact options than generic homepage-only results

## Validation Checks

Before finalizing the pack:

- Verify every company has a working public URL.
- Verify every company has at least one usable public contact path or a documented homepage fallback.
- Remove duplicates and brand/location overlaps unless both are intentionally distinct.
- Check that outreach angles are based on the public evidence, not generic assumptions.
- If a claim cannot be traced to a source, drop it.

## Output Discipline

- Do not rely on private datasets, hidden contact stores, or unverifiable scraped claims.
- Keep notes concise and source-backed.
- Prefer breadth over overfitting.
- Use `medium` confidence when the company fits but the signal is thin.
- Use `low` confidence only when the pack needs to preserve a borderline candidate and the gap is explicitly noted.
