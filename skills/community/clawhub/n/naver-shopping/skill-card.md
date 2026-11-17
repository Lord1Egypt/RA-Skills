## Description:

Search for products on Naver Shopping. Use when the user wants to find product prices, links, or compare items in the Korean market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dryoo](https://clawhub.ai/user/dryoo)

### License/Terms of Use:


## Use Case:

External users, shopping researchers, and agents use this skill to query Naver Shopping for product listings, prices, links, and Korean-market comparisons through the Naver Search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Naver Search API credentials are required in the agent environment.

Mitigation: Install only where providing NAVER_Client_ID and NAVER_Client_Secret is acceptable, and keep credentials in environment configuration rather than prompts or shared output.

Risk: The documented command path is user-specific and may not match the installed skill location.

Mitigation: Adjust commands to the installed skill path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dryoo/skills/naver-shopping)
- [Naver Shopping Search API endpoint](https://openapi.naver.com/v1/search/shop.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON search results printed to stdout, with concise command and environment-variable guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NAVER_Client_ID and NAVER_Client_Secret environment variables; display and sort options control result count and ordering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
