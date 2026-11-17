## Description:

[Didoo AI] Analyzes Meta Ads audience efficiency across audience types, overlap, demographics, and budget allocation. Use when reviewing targeting strategy, planning audience expansion or narrowing, or auditing budget distribution across audience segments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and analysts use this skill to review Meta Ads audience efficiency, overlap, demographic performance, placement results, and budget allocation before campaign planning or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Meta access token with broader permissions than needed could expose campaign data beyond the skill's read-only analysis use case.

Mitigation: Use a token limited to the read-only ads_read scope before running the skill.

Risk: Campaign-derived audience and budget findings are written to session context for use by the related recommendation skill.

Mitigation: Run the skill only when that session-context handoff is acceptable for the account and campaign data being analyzed.

Risk: Audience segment conclusions can be misleading when based on too little data.

Mitigation: Follow the skill's minimum of 50 results per segment before drawing conclusions on an audience slice.

## Reference(s):

- [Didoo AI Blog](https://didoo.ai/blog)
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/skills/meta-ads-audience-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with structured sections and session-context findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audience issues and budget reallocation findings to session context for the related recommendation skill.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
