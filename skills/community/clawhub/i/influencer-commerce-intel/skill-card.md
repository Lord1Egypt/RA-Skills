## Description:

TikTok Shop Commerce Intelligence helps agents analyze product selection and creator commerce signals, including sales, GMV, goods, live, video-ad, and product-detail data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce analysts, marketers, and agent users use this skill to assess TikTok Shop creator performance, product opportunities, monetization durability, and pilot recommendations from sales, goods, live, and video-ad signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can send credentials and requests to a configurable API endpoint.

Mitigation: Use only a trusted HTTPS SCRUMBALL_BASE_URL, scope SCRUMBALL_API_KEY to this workflow, and avoid storing unrelated secrets in local .env files.

Risk: The runner creates and sends a persistent install identifier.

Mitigation: Review and accept this behavior before installing, or remove or patch the install ID behavior if persistent tracking is not acceptable.

Risk: Commerce signals may be incomplete when identifiers or dimensions are missing.

Mitigation: Ask for required identifiers, continue only with available dimensions, and lower confidence when the data sample is limited.

## Reference(s):

- [API Index](references/api-index.md)
- [Request and Response Guide](references/request-response.md)
- [Operations Manifest](references/operations.json)
- [ClawHub Skill Page](https://clawhub.ai/chengyu-xixihaha/skills/influencer-commerce-intel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected sections include Commerce summary, Opportunity, Risk, and Next step.]

## Skill Version(s):

1.0.3 (source: server release metadata and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
