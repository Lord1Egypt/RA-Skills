## Description:

Specialized analysis module for Meta lead generation campaigns when CPL is elevated, lead quality is unclear, or downstream conversion diagnosis is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts, media buyers, and agent operators use this skill to diagnose Meta lead generation campaigns with elevated CPL, unclear lead quality, or weak downstream conversion, including CAPI status, audience fit, and funnel bottlenecks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta ads access token and ad account ID to inspect campaign and form integration data.

Mitigation: Use a read-only token with the documented ads_read scope and rotate or revoke credentials according to the organization's normal access process.

Risk: Campaign diagnostics may be stored in session context for a companion recommendation skill.

Mitigation: Review session context before reuse and avoid placing sensitive lead, customer, or CRM records into the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-lead-gen-analysis)
- [Didoo AI blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with session-context key summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store session context keys for lp_diagnosis, capi_status, cpl_breakdown, and recommended_fix_priority.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
