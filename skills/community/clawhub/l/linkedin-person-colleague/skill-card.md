## Description:

Find internal colleagues through company ID and personnel ID on LinkedIn to map organizational structures and gather contacts for sales outreach and account intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, sales teams, and B2B lead-generation specialists use this skill to look up colleagues for a known LinkedIn company ID and person ID, map team networks, and expand account-intelligence contact lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags paid-account credentials, top-up orders, and telemetry for review.

Mitigation: Use a safer secret mechanism for the API key where possible, avoid printing or sharing ~/.upkuajing/.env, and confirm paid queries or top-up actions before execution.

Risk: LinkedIn colleague lookup can involve personal and organizational contact data for sales outreach or contact expansion.

Mitigation: Confirm the user's privacy, legal, and policy basis before collecting, using, or sharing returned colleague data.

Risk: Error reporting sends troubleshooting context to the platform and may include request metadata.

Mitigation: Ask for user confirmation before reporting abnormal calls and avoid including unnecessary sensitive context.

## Reference(s):

- [Colleague List API Reference](references/linkedin-person-colleague-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/linkedin-person-colleague)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY and explicit confirmation before fee-incurring calls.]

## Skill Version(s):

1.0.5 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
