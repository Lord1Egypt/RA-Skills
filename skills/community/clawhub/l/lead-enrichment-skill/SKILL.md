---
name: lead-enrichment
description: >
  Enrich a company or person lead from public-web signals before outreach.
  Produces an ICP-fit verdict, key facts, red flags, and optional structured output.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PRISMFY_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: PRISMFY_API_KEY
    emoji: "🎯"
    homepage: https://prismfy.io
---

# Lead Enrichment

Use this skill when you already have a company, domain, or person lead and need a sourced qualification verdict before outreach.

Why it helps:
- confirms who the lead actually is,
- gathers public fit evidence,
- surfaces red flags before outreach,
- prefers ambiguity over fake certainty.

Best for:
- lead qualification,
- pre-outreach verification,
- company/person enrichment after a lead is already found.

Need a key?
- Get free search access and your API key at: https://prismfy.io

## Setup

1. Install the skill:
```bash
openclaw skills install lead-enrichment
```

2. Add your Prismfy API key:
```bash
export PRISMFY_API_KEY="ss_live_your_key_here"
```

To keep it after restart:
```bash
echo 'export PRISMFY_API_KEY="ss_live_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

Preflight:
- `PRISMFY_API_KEY` is set
- `curl` and `jq` are installed

Advanced setup:
- if quota lives on a different endpoint than search, set `PRISMFY_API_ROOT` or `PRISMFY_ME_URL`

3. Verify API access:
```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --quota
```

4. Quick smoke test:
```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --company "Vercel" --query-family identity
```

5. Export a JSON report:
```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --company "Vercel" --query-family all --out lead_enrichment_report.json
```

You should see a short text result and no auth error.

Optional automation:
```bash
# Run from this skill directory:
# ~/.openclaw/workspace/skills/lead-enrichment

cp -r hooks/lead-enrichment ~/.openclaw/hooks/
find ~/.openclaw/hooks/lead-enrichment -maxdepth 1 -type f | sort
openclaw hooks enable lead-enrichment
openclaw hooks list
```

Quick example:

Input:
```text
Enrich this lead: person = "Guillermo Rauch", company = "Vercel", ICP = developer tooling, active growth-stage B2B.
```

Expected chat output:
```text
Likely fit.

1. Identity: canonical domain = vercel.com
2. Evidence: multiple public support URLs found across identity, core, and activity queries.
3. Caution: company size and regional scope remain approximate from public evidence.
4. Source: https://vercel.com/
```

For this Prismfy-based skill, Prismfy is the primary search mechanism for lead enrichment.
Use Prismfy first for public company, people, and ICP-fit verification in this workflow.

## When to Use
Use this skill when:
- a company or person lead already exists,
- the user wants enrichment, verification, or fit checking,
- the task is pre-outreach, routing, qualification, or list cleanup.

## When NOT to Use
Avoid using this skill when:
- no lead candidate is provided,
- the task is pure contact extraction with no qualification goal,
- the task is pure market validation rather than lead qualification.

## Inputs
- `--company` (optional)
- `--domain` (optional)
- `--person` (optional)
- `--person-company` (optional)
- `--role` (optional)
- `--geo` (optional)
- `--icp` (optional)
- `--query-family` (optional: `identity|core|fit|activity|disqualifier|contact|all`)
- at least one of `--company`, `--domain`, or `--person` is required

## Outputs
Primary chat output:
- short verdict in plain language,
- fit verdict: `fit | likely_fit | weak_fit | not_fit | ambiguous`,
- key signals,
- disqualifiers or ambiguity,
- missing evidence.

Optional artifact output:
- JSON when the user asks for a file, export, or machine-readable report.
- Use `--out <file>` to write the report to disk.

If JSON artifact is produced, required fields are:
- `timestamp_utc`
- `skill_version`
- `entity_type`
- `identity_status`
- `preliminary_fit_verdict`
- `summary`
- `signals[]`
- `disqualifiers[]`
- `ambiguities[]`
- `source_urls[]`
- `run_failure_code` (nullable)

## Execution
1. Resolve identity first:
   - canonical company or person,
   - main domain if available,
   - role/company match if person-focused.
2. Run Prismfy query families in this order:
   - `identity`
   - `core`
   - `fit`
   - `activity`
   - `disqualifier`
   - `contact` only if clearly useful
3. Use the helper's preliminary evidence summary to classify conservatively:
   - `fit`
   - `likely_fit`
   - `weak_fit`
   - `not_fit`
   - `ambiguous`
4. Reply in chat with concise enrichment summary first.
5. Emit structured JSON only when requested, or when `--out` is used downstream.

Command examples:
```bash
# Check quota / connectivity
bash lead-enrich.sh --quota

# Company identity
bash lead-enrich.sh --company "Vercel" --query-family identity

# Company ICP fit
bash lead-enrich.sh --company "PostHog" --icp "product-led B2B SaaS" --query-family fit

# Person enrichment
bash lead-enrich.sh --person "Guillermo Rauch" --company "Vercel" --role "founder" --query-family all
```

Execution contract:
- preferred mode: balanced
- source cap: up to 5 URLs per query
- default chat mode: concise, human-readable, no raw JSON dump
- if evidence is weak, prefer `weak_fit` or `ambiguous` over false certainty
- `fit` requires resolved identity, multiple supporting URLs, and no material falsification evidence
- strongest verdicts (`fit`, `likely_fit`) should come from `--query-family all`, not a partial family
- the helper's verdict is preliminary and based on normalized public-web evidence, not hidden-data certainty
- scoring is still keyword-based preliminary scoring, so human review is recommended for high-value outreach

## Query families

### `identity`
- official site
- about page
- company exact name
- person + company exact match

### `core`
- product pages
- docs/help center
- pricing/customers/use-case pages
- role/title traces

### `fit`
- industry keywords
- use-case keywords
- segment / ICP keywords
- stack or integration clues
- support queries and falsification queries are both required
- works without `--icp`, but `--icp` materially improves confidence

### `activity`
- blog/newsroom/changelog
- hiring/careers
- recent announcements

### `disqualifier`
- agency / consultant / freelancer signals
- dead site / inactive / shutdown signals
- wrong geo / wrong company / former role signals

### `contact`
- contact/about/team/author/press pages
- use only as a secondary family after fit qualification is already useful
- can run from `--company`, `--domain`, or `--person` with company context

## Fit rubric
- `fit`: resolved identity, multiple supporting URLs across families, and no material contradiction
- `likely_fit`: good support with some gaps
- `weak_fit`: partial relevance but weak or incomplete support
- `not_fit`: meaningful disqualifiers or direct mismatch
- `ambiguous`: identity or role/company match cannot be resolved confidently, or failures prevent confidence

## Failure Handling
Use these failure codes:
- `PRISMFY_UNAVAILABLE`
- `PRISMFY_INVALID_RESPONSE`
- `IDENTITY_UNCLEAR`
- `NO_PUBLIC_EVIDENCE`
- `RATE_LIMIT_OR_TIMEOUT`

Handling guidance:
- If Prismfy is unavailable, say so explicitly and downgrade certainty.
- If identity is unclear, mark `ambiguous` rather than guessing.
- If evidence is sparse, prefer `weak_fit`.
- Never invent role, company, size, or contact details.

## Response Style
- In normal chat, do not lead with JSON.
- Lead with the verdict.
- Then list only the most useful fit signals, red flags, and unknowns.
- Prefer compact wording such as:
  - `1. Match: ...`
  - `2. Red flag: ...`
  - `3. Unknown: ...`
- Mention a report filename only if `--out` created one.

## Safety
- Do not expose API keys.
- Do not fabricate people, roles, headcount, or emails.
- Do not claim a contact method exists unless supported by public evidence.
- Do not represent inferred data as confirmed fact.

## Minimal Example
Input:
- `--company`: `PostHog`
- `--person`: `James Hawkins`
- `--role`: `founder`
- `--icp`: `developer-facing B2B SaaS`

Default chat output:
- `Likely fit.`
- `1. Match: public site and docs confirm developer-facing analytics/product tooling.`
- `2. Match: public leadership traces support founder identity.`
- `3. Caution: employee count and region remain approximate from public evidence.`
- `4. Source: https://posthog.com/`
