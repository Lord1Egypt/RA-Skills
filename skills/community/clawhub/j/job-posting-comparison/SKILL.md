---
name: job-posting-comparison
description: Compare advertised job postings using Crawlora jobs datasets, employer ATS boards, and Indeed detail. Use for a role shortlist or posting comparison with employer/requisition identity, location, seniority, compensation units, transport-dependent fields, and offer limits preserved.
---

# Job posting comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Build a candidate-facing comparison of advertised roles. Establish desired
function, seniority, geography/workplace constraints, compensation basis, and
must-have requirements. A posting is an advertised role, not a negotiated offer.

## Discover and verify postings

1. Discover dataset provider/workplace/department values, then collect a bounded
   role set. Stored roles are open by default but can lag live boards. Resolve
   provider-specific posting IDs, employer/domain, requisition and location before
   detail. Dataset IDs, Indeed `job_key`, and ATS IDs are separate namespaces.
2. Use `jobs_company_search` for supplied company slugs, then the actual detected
   provider's board/detail route. Include full posting content when available and
   keep exact required slug/token/company fields. A guessed ATS slug is not proof
   that a board belongs to the employer; verify its official identity.
3. Preserve title/responsibilities, required versus preferred qualifications,
   location/remote scope, employment type, salary text and normalized currency/
   period, benefits and source dates. Indeed's GraphQL response can omit remote,
   employment type and benefits even when page transport supplies them; missing
   fields are unknown rather than a denial. Some dataset providers omit dates/types.
4. Deduplicate by actual requisition/provider ID with location evidence. Multiple
   geographic versions can be one role; evergreen/pipeline listings are not a
   count of filled or actively funded vacancies. Expired/failed detail leaves
   unavailable evidence rather than proof the employer stopped hiring.

```sh
scripts/crawlora.sh /datasets/jobs/facets
scripts/crawlora.sh /datasets/jobs/search q="backend engineer" page=1 page_size=10
scripts/crawlora.sh /indeed/search q="backend engineer" l="Austin, TX" page=1
# Use verified returned posting IDs and provider-specific selectors for detail.
```

## Compare the same compensation and requirement basis

Salary-bounded dataset queries require `salary_currency` and expose no salary-period
selector: inspect and normalize period after retrieval rather than assuming every
bound is annual. Ranges use overlap
semantics, not proof every possible offered salary meets the user's minimum.
Keep hourly/monthly/annual, base/bonus/equity, gross/net, currency and regional
bands separate. Annualize only with declared hours/weeks/basis assumptions;
unknown equity, commissions, fees, tax and relocation costs remain unknown.
A posted upper range is not an expected individual offer or take-home pay.

Return an employer/requisition ledger, requirements-and-compensation matrix,
fit evidence and questions. Separate source wording from classifier-derived
seniority/occupation labels; ambiguous roles need review rather than automatic
exclusion. Use the user's criteria and disclosed weights, not employer popularity.
Do not apply, upload a CV, contact recruiters, infer visa eligibility from silence,
or negotiate terms unless the user requests those actions.
