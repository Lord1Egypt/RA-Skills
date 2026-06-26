---
name: ocean-io
version: 1.0.0
description: >
  B2B prospecting and lookalike intelligence powered by Ocean.io.
  Find companies similar to your best customers, identify decision-makers
  by title and seniority, and export enriched lists directly to your workflow.
author: ocean-io
tags:
  - prospecting
  - sales
  - gtm
  - b2b
  - lead-generation
  - abm
  - lookalike
platforms:
  - macos
  - linux
  - windows
mcp_servers:
  - name: ocean-mcp
    url: https://api.ocean.io/mcp/?api-token=${OCEAN_API_TOKEN}
env:
  OCEAN_API_TOKEN:
    description: "Your Ocean.io API token. Get it at app.ocean.io → Settings → API."
    required: true
---

## Overview

This skill connects your OpenClaw agent to Ocean.io's B2B intelligence platform. Use it to build prospect lists, enrich accounts, find lookalike companies, and surface the right contacts — all from natural language commands.

Ocean.io covers 60M+ companies and 200M+ people. Credits are consumed at 0.2 per record for both searches and exports.

---

## When to use this skill

Activate Ocean.io when the user wants to:

- Find companies similar to existing customers ("lookalike" search)
- Build a prospect list filtered by industry, size, location, or tech stack
- Identify decision-makers at target accounts by title, department, or seniority
- Export a contact or company list to CSV for use in outreach tools
- Check what fields are available before building a search

---

## Tools

### `search_companies`
Find companies matching ICP criteria or similar to a set of seed domains. Use `lookalike_domains` when the user wants to replicate their best customers.

Key filters available:
- `lookalikeDomains` — up to 10 seed domains to find similar companies
- `companyMatchingMode` — `"precise"` (same product/service) or `"broad"` (same industry)
- `industries`, `industryCategories` — firmographic segmentation
- `companySizes` — e.g. `["51-200", "201-500"]`
- `primaryLocations` / `otherLocations` — HQ country or office presence
- `technologies.apps` / `technologies.categories` — tech stack filters
- `headcountGrowth` — growth signal over 3, 6, or 12 months
- `fundingRound` — type, amount, and date of last funding
- `revenues` — revenue band filter
- `webTraffic` — monthly visits/views range
- `excludeDomains` — exclude known customers or competitors

Always check `list_company_fields` if the user asks what data is available.

---

### `search_people`
Find people by job title, seniority, department, or company criteria. The `people_fields` parameter is **required** — always specify what to return.

Key filters available:
- `jobTitleKeywords` — keyword match on title (allOf / anyOf / noneOf)
- `seniorities` — Owner, Founder, C-Level, VP, Head, Director, Manager, Other
- `departments` — Sales, Marketing and Advertising, Engineering, Product, etc.
- `countries` / `cities` / `states` — geographic filters
- `company_filters` — nest any `search_companies` filters to target people at specific accounts
- `changedPositionAfter` — recently promoted/hired contacts (format: "YYYY-MM")
- `lookalikeLinkedinHandles` — find people similar to a given LinkedIn profile
- `skills` — filter by LinkedIn-listed skills
- `connections` — filter by LinkedIn connection count

Always check `list_people_fields` if the user asks what data can be returned.

---

### `export_companies`
Export company records to a CSV file. Returns a **download URL** for the generated file.

⚠️ **Costs credits**: 0.2 credits per successfully exported company. Always confirm the number of records and estimated credit cost with the user before calling this tool.

Input: array of company `domains`. Accepts up to **10,000 domains** per request.

---

### `export_people`
Export people records to a CSV file. Returns a **download URL** for the generated file.

⚠️ **Costs credits**: 0.2 credits per successfully exported person. Always confirm the number of records and estimated credit cost with the user before calling this tool.

Input: array of LinkedIn handles or URLs (from `search_people` results). Accepts up to **10,000 per request**.

---

### `list_company_fields`
Returns all available fields for company records. Output is static — call **once per session and cache the result**. Do not call again if already retrieved. Use when the user asks "what data does Ocean.io have on companies?"

---

### `list_people_fields`
Returns all available fields for people records. Output is static — call **once per session and cache the result**. Use when the user asks "what fields can I get for contacts?"

---

### `list_industries` / `list_linkedin_industries`
Returns valid industry values for filters. Output is static — call **once per session and cache the result**. Always validate industry names against this list before passing them to search filters.

---

## Example workflows

### ICP lookalike prospecting
> "Find 20 companies similar to stripe.com and shopify.com, B2B SaaS, 50-500 employees, US-based."

1. Call `search_companies` with `lookalikeDomains: ["stripe.com", "shopify.com"]`,
   `companySizes: ["51-200", "201-500"]`, `primaryLocations: { includeCountries: ["us"] }`.
2. Present results as a table (name, domain, size, industry, country).
3. Confirm credit cost (N × 0.2) before calling `export_companies`.

---

### Finding decision-makers at target accounts
> "Find VP of Sales or Head of Revenue at these 10 companies."

1. Call `search_people` with `jobTitleKeywords: { anyOf: ["VP of Sales", "Head of Revenue"] }`,
   `seniorities: ["VP", "Head"]`, `company_filters: { includeDomains: [...] }`,
   `people_fields: ["name", "jobTitle", "linkedinUrl", "country", "departments"]`.
2. Display results as a table.
3. Offer to export — confirm credit cost before calling `export_people`.

---

### Trigger-based prospecting (recently funded)
> "Find Series A or B SaaS companies that raised funding in the last 6 months."

1. Call `search_companies` with `fundingRound: { types: ["Series A", "Series B"], date: { from: "<6 months ago>" } }`.
2. Optionally layer in industry/size filters if the user specifies an ICP.
3. Suggest following up with `search_people` to find the relevant contacts at those accounts.

---

### Hiring signal prospecting
> "Find companies in the sales tech space that are rapidly growing their Sales department."

1. Call `search_companies` with `departmentHeadcountGrowth` targeting the Sales department
   with positive growth over the last 6 months.
2. Cross-reference with industry or tech stack filters to narrow to ICP.

---

### Full account + contact workflow with export
> "Find Chicago-headquartered companies similar to pandadoc.com and export them to CSV."

1. Call `search_companies` with `lookalikeDomains: ["pandadoc.com"]`, `primaryLocations: { includeCountries: ["us"] }`, and a city filter for Chicago.
2. Present results as a table (name, domain, description).
3. State: "This export will consume X credits (N companies × 0.2). Confirm?"
4. On confirmation, call `export_companies` and return the **download URL** to the user.

---

## Credit awareness

**All operations consume credits at 0.2 credits per record** — this applies to both search results and exports. Before any search, state the estimated credit cost (num_results × 0.2). Before any export, confirm: "This will export N records at 0.2 credits each = X credits total. Confirm?"

Never call `export_companies` or `export_people` without explicit user confirmation.

---

## Tips

- Use `companyMatchingMode: "precise"` for tight lookalikes (same product category).
  Use `"broad"` when the user wants a wider net (same industry vertical).
- Combine `search_companies` + `search_people` for full account + contact workflows:
  find the companies first, then pass their domains into `company_filters.includeDomains`
  on `search_people`.
- `changedPositionAfter` is powerful for timing outreach — a newly hired VP of Sales
  is actively building their stack.
- Both `search_companies` and `search_people` return **paginated results**. After presenting the first page, offer to load more. Pass the `searchAfter` token from the last result into the next call to fetch the next page.
- For pagination, pass the `searchAfter` value from previous results back into the next call.
