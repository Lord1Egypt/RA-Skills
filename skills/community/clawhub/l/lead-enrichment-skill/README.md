# Turn Raw Leads into Sourced Fit Verdicts

`lead-enrichment` turns a company, domain, or person into a public-web qualification verdict before outreach.

Built for outbound and qualification workflows, it checks identity, ICP match, activity, and red flags, then returns a concise fit-or-no-fit summary with source-backed evidence.

You give:
- `company`, `domain`, or `person + company`

You get:
- canonical identity
- preliminary fit verdict
- top supporting signals
- red flags and ambiguity
- source URLs
- optional JSON when you ask for export mode

Powered by Prismfy web search. Get your API key at [prismfy.io](https://prismfy.io).

## Example

Input:

```text
Enrich this lead: company = "PostHog", person = "James Hawkins", role = "founder", ICP = product-led B2B SaaS, active growth-stage team.
```

Expected result:

```text
Likely fit.

1. Identity: canonical domain = posthog.com
2. Evidence: identity resolved, product/docs/hiring traces found, multiple public support URLs.
3. Caution: employee count and regional scope remain approximate from public evidence.
```

## What it does

Given a company, domain, or person, this skill:
1. resolves identity,
2. collects public company or role facts,
3. tests support and falsification signals,
4. checks activity and recency,
5. flags disqualifiers,
6. returns a concise preliminary verdict,
7. optionally writes a structured JSON artifact.

The default behavior is chat-first. It should answer like an analyst, not dump raw JSON unless you asked for an export.
Use `--out <file>` when you want a saved JSON report.

## Setup

### 1. Install the skill

```bash
openclaw skills install lead-enrichment
```

### 2. Add your Prismfy API key

```bash
export PRISMFY_API_KEY="ss_live_your_key_here"
```

To keep it after restart:

```bash
echo 'export PRISMFY_API_KEY="ss_live_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Preflight

- `PRISMFY_API_KEY` is set
- `curl` and `jq` are installed

### 4. Verify API access

```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --quota
```

Advanced setup:
- if quota lives on a different endpoint than search, set `PRISMFY_API_ROOT` or `PRISMFY_ME_URL`

### 5. Quick smoke test

```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --company "Vercel" --query-family identity
```

You should see a short text result and no auth error.

### 6. Export a JSON report

```bash
cd ~/.openclaw/workspace/skills/lead-enrichment
bash lead-enrich.sh --company "Vercel" --query-family all --out lead_enrichment_report.json
```

## Optional automation

Recommended if you want OpenClaw to remember this workflow more consistently.

```bash
# Run from this skill directory:
# ~/.openclaw/workspace/skills/lead-enrichment

cp -r hooks/lead-enrichment ~/.openclaw/hooks/
find ~/.openclaw/hooks/lead-enrichment -maxdepth 1 -type f | sort
openclaw hooks enable lead-enrichment
openclaw hooks list
```

## Included files

- `SKILL.md` — OpenClaw skill instructions
- `lead-enrich.sh` — bundled Prismfy query helper
- `hooks/lead-enrichment/` — optional bootstrap reminder hook

## Important MVP note

This skill is designed as evidence-backed enrichment, not a hidden-data enrichment vendor replacement.

It works from public-web signals found through Prismfy. The verdict is intentionally preliminary and should default to ambiguity when identity or fit evidence is weak.
Scoring is still keyword-based preliminary scoring, so human review is still recommended for high-value outreach.
Use `--query-family all` when you want the strongest fit verdict.
