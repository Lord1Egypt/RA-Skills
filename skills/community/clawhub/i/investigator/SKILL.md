---
name: osint-investigator
description: Investigate public online footprints using open-source intelligence techniques. Use when a user wants to research a username, email, person, company, domain, IP, phone number, location, image, or other public target using publicly available information; correlate findings; validate profile candidates; enrich results with web search; capture public profile links and profile images; run optional defensive HIBP email checks when configured; or export structured JSON and reports.
---

# OSINT Investigator

Use this skill for broad public-footprint OSINT.

Supported target types include:
- username / handle
- email address
- person / alias
- organisation / company
- domain / website
- IP address
- phone number
- location / address
- image

Read as needed:
- `references/target-types.md` for classification
- `references/workflow.md` for investigation flow
- `references/modules.md` for module selection
- `references/osint-sources.md` for source categories
- `references/platforms.md` for target platforms and search ideas
- `references/platform-validation.md` for platform-specific validation rules
- `references/profile-media.md` for profile image handling
- `references/scoring.md` for confidence logic
- `references/aggregation.md` for overall scoring and result merging
- `references/variants.md` for handle-variant generation
- `references/tooling.md` for lightweight discovery helpers
- `references/breach-checks.md` for optional defensive breach lookup behavior
- `references/apis.md` for optional API enrichment
- `references/configuration.md` for HIBP API key setup
- `references/report-format.md` for structured reporting
- `references/safety.md` for acceptable-use boundaries
- `references/output.md` for response structure

Use scripts when helpful:
- `scripts/generate_variants.py` for plausible username variants
- `scripts/check_profiles.py` for first-pass platform checks with platform-aware validation
- `scripts/check_hibp.py` for optional Have I Been Pwned email checks
- `scripts/check_domain.py` for lightweight domain enrichment
- `scripts/check_ip.py` for lightweight IP enrichment
- `scripts/aggregate_results.py` to merge findings into a scored summary
- `scripts/export_json.py` for structured JSON output
- `scripts/build_report.py` for compact report generation from structured results

Use `web_search` and `web_fetch` to confirm weak findings, enrich strong ones, and gather public evidence when helper-script results alone are ambiguous.

## Core behavior

- Focus on public data only.
- Prefer lightweight verification over aggressive scraping.
- A 200 HTTP status is not enough to confirm a profile.
- Separate facts from guesses.
- Report confidence, not certainty.
- Keep results structured and easy to audit.
- Prefer a smaller set of verified findings over a noisy wall of guesses.
- Run only the modules relevant to the target.

## Workflow

1. Classify the target using `references/target-types.md`.
2. Normalize the input.
3. Select relevant modules using `references/modules.md`.
4. Run lightweight helper scripts where useful.
5. Use targeted web search to confirm or enrich weak and likely matches.
6. Capture final links and public profile image URLs when available.
7. If an email is provided and HIBP is configured, run a defensive breach check.
8. For domains or IPs, run the relevant lightweight helper.
9. Record exact matches, likely matches, weak matches, no-results, and not-verifiable results.
10. Compare public signals across findings.
11. Aggregate the findings into a scored summary using `scripts/aggregate_results.py` and `references/aggregation.md`.
12. Return a concise human summary or a structured report depending on the request.
13. Export JSON if requested.

## Output rules

Always distinguish between:
- confirmed public match
- likely match
- weak/uncertain match
- not verifiable
- no evidence found

Include final links for meaningful findings.
Include profile image links only when they are publicly exposed and easy to extract.
If HIBP is used, report breach results as defensive exposure information, not identity proof.
If using domain/IP helpers, treat them as enrichment, not full attribution.

Do not overclaim identity resolution.
If evidence is thin, say so clearly.
If evidence conflicts, say so clearly.
Lead with the strongest public evidence first.
Prefer the compact format by default; use an extended report only when the user asks for depth.

## Safety

Read `references/safety.md` when the request could drift into harassment, private-person targeting, or invasive tracking.

Do not help with:
- credential theft
- account takeover
- bypassing access controls
- doxxing
- stalking or targeted harassment
- collecting non-public personal data
- invasive private-person targeting

## Style

- concise
- factual
- audit-friendly
- explicit about uncertainty
