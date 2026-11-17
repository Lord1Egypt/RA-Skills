---
name: hiring-demand-analysis
description: Compare advertised hiring demand across roles, skills, locations, and seniority using Crawlora's jobs dataset. Use for labor-market snapshots, employer concentration, remote-work comparisons, and salary analyses with explicit coverage and compensation-unit controls.
---

# Hiring demand analysis

Measure the advertised openings observed in a defined corpus. Postings are not
completed hires, headcount growth, unique vacancies, or the entire labor market.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
jobs search, global facets, company discovery, and posting detail.

## Define the population before counting

1. Specify the role/skill question, locations, providers, employment/workplace
   scope, observation date, and required sample coverage. Search
   `/datasets/jobs/search`; open roles are the default. `include_closed=true`
   adds stored closed roles but does not reconstruct past point-in-time vacancies.
2. Read `/datasets/jobs/facets?size=...` for corpus context and labels. **This
   endpoint accepts only bucket size, not search filters.** Its `total_open`,
   `remote_open`, and buckets are global. Do not use them as the denominator or
   skill distribution for a filtered search. Buckets are capped, not exhaustive.
3. Use search fields that actually exist: `q` spans title/company/description;
   `city`, `state`, `country`, `department`, and `job_family` have their documented
   matching behavior. `workplace_type` accepts `onsite`, `hybrid`, `remote`.
   Skill and seniority facets are not equivalent to server-side search filters.
   Inspect/classify returned rows when those dimensions define the analysis.
4. Collect within the agreed bound (`page_size<=100`, 10,000-result window).
   Preserve `posting_id`, provider, employer, URL, raw location, structured fields,
   posted date, open status, and available crawl timestamps. Deduplicate by posting
   ID, then identify likely syndicated/reposted roles using employer, requisition,
   title, location, and canonical URL. Keep ambiguous multi-location roles explicit.
5. For skill demand, distinguish required, preferred, and incidental mentions;
   a keyword hit in a company description is not necessarily a job requirement.
   Treat `seniority_level` and occupation fields as classifications, not employer
   assertions. Seniority is `entry`, `mid`, or `senior`, with uncertain roles
   assigned to `mid`; ambiguous occupations may lack a `job_family` entirely.
6. For compensation, retain `compensation_min`, `compensation_max`, currency,
   period, and source wording. `min_salary`/`max_salary` require `salary_currency`
   and match overlapping range bounds, not guaranteed pay. Currency filtering
   alone does not normalize hourly/monthly/annual figures; verify period locally.
   Do not annualize without explicit hours/weeks assumptions or treat base salary
   as total compensation. Report pay-disclosure coverage before summaries.
7. Return counts and proportions with a defined denominator: deduplicated
   eligible observed postings, unique employers, or salary-disclosing rows.
   Multi-skill labels can total above 100%. Label truncated samples and corpus
   gaps; raw search `total` is not the deduplicated population size.

```sh
scripts/crawlora.sh /datasets/jobs/facets size=10
scripts/crawlora.sh /datasets/jobs/search q="data engineer" page_size=20
```

## Interpretation and reporting

Return query/cohort definitions, coverage and exclusions, counts by relevant
dimension, cited example postings, and limitations. A one-time snapshot describes
observed demand; trend claims require comparable dated snapshots and stable coverage.

- Structured locations can be missing while enrichment catches up. Missing is
  not remote, and remote does not mean eligible from every country.
- Some providers omit employment type or posting dates. Do not equate ingestion
  date with publication date or classify undated roles as newly opened.
- Historical employer visa filings, if returned, are not a role-specific promise.
  Keep this contextual evidence separate from the demand analysis.
- Salary summaries describe advertised ranges among disclosing postings, not
  accepted compensation or a representative wage survey. State midpoint choices.
- Back off on `429`, retry transient `5xx` once, stop on `401`/`403`, and check
  application `code`. Stop on repeated pages; research does not apply to jobs or
  contact employers, and a snapshot request does not create ongoing monitoring.

## Current search context

For a current multi-employer search sample, use `google_jobs` separately from
stored dataset counts. It calls POST `/google/jobs` with a flat JSON body, for
example:

```sh
scripts/crawlora.sh -X POST /google/jobs '{"query":"software engineer","location":"San Francisco, CA","page":1}'
```

This is Google's aggregated job-search surface, distinct from Google's own
careers site at `/google-jobs/search`. Returned snippets are discovery leads;
verify the employer and posting before using them. Keep this bounded search
sample separate from stored job-dataset denominators, refresh dates, and demand
calculations. Do not infer a filled vacancy or absent demand from an empty result.
