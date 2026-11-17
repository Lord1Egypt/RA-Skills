## Description:

Provides real-time DXY and US10Y macro-financial data for agent workflows, with SkillPay micro-billing declared by the release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longxrise](https://clawhub.ai/user/longxrise)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, analysts, and investment research workflows use this skill to fetch macro-market signals for pre-trade checks, research article data pulls, and automated macro dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing-sensitive calls rely on a caller-supplied user_id while the manifest declares no authentication.

Mitigation: Use only where the provider documents authenticated and signed payment authorization, replay protection, strict request validation, and privacy handling for user_id.

Risk: The OpenAPI request schema allows arbitrary additional properties and does not document a typed response schema.

Mitigation: Validate inputs and outputs in the calling agent, and avoid automated trading or billing actions based solely on the response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longxrise/skills/macro-driver-pro)
- [OpenAPI specification](https://macro-driver-pro.vercel.app/openapi.json)
- [Legal information URL declared in manifest](https://github.com/longxrise/macro-driver-pro#readme)
- [Source code URL declared in manifest](https://github.com/longxrise/macro-driver-pro)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [API response containing a macro-financial report; the OpenAPI response schema is not specified.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No authentication is declared; /api/v1/macro-report accepts an open JSON object and may require user_id for billing.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
