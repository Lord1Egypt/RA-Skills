## Description:

Queries IP security intelligence and threat-IP data, including geolocation, risk scoring, proxy/VPN/Tor checks, blacklist context, ASN details, and daily, weekly, monthly, or threat-report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanzx3](https://clawhub.ai/user/yanzx3)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident responders, and operations teams use this skill to query IP threat intelligence through an external API and draft security situation reports from threat statistics and top-risk IP data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP indicators submitted to the ai2api.top service may disclose sensitive investigation or customer context.

Mitigation: Use the skill only when disclosure to that provider is approved, and avoid submitting private, customer-sensitive, or incident-confidential IP data.

Risk: API keys can be exposed if copied into prompts, code, or configuration files.

Mitigation: Store IP_INTELLIGENCE_API_KEY in the environment, use a scoped and revocable key, and do not hardcode credentials.

Risk: Generated threat reports may contain incomplete or time-sensitive intelligence.

Mitigation: Review report content and validate high-impact findings before blocking, escalation, or stakeholder distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanzx3/skills/ip-intelligence)
- [IP intelligence API endpoint](https://ai2api.top/api/v1/security/ip-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown reports, plain-language guidance, and JSON API request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IP_INTELLIGENCE_API_KEY for authenticated API access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
