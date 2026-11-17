## Description:

Validates phone numbers through Upkuajing's API and returns validity, number type, country code, and WhatsApp registration status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as sales teams, recruiters, traders, and CRM operators use this skill to clean contact lists and screen phone numbers before outreach. It helps classify phone numbers and WhatsApp status so users can reduce invalid contacts before CRM updates, candidate screening, supplier checks, or campaign preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers submitted for validation are sent to the Upkuajing service.

Mitigation: Use the skill only when the user trusts Upkuajing with the submitted phone numbers and the intended validation purpose.

Risk: The skill uses a paid API key stored in or loaded from ~/.upkuajing/.env.

Mitigation: Do not print the key in terminal output or chat, store it with restrictive file permissions, and rotate it if it is exposed.

Risk: Phone validation and recharge flows can incur costs.

Mitigation: Require explicit user confirmation before paid validation, API-key creation that affects account setup, or recharge-order actions.

Risk: The security evidence flags billing flows and update checks as behavior users should review before installing.

Mitigation: Review the skill before installation and confirm the network, billing, and version-check behavior matches the user's operating expectations.

## Reference(s):

- [Phone validation API reference](references/phone-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/phone-validity-check-zh)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON validation results with natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid validation and recharge actions require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
