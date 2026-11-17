## Description:

Use this skill for CurrencyBeacon currency conversion and for retrieving currency lists and exchange-rate data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents with a connected CurrencyBeacon account use this skill to convert currencies and retrieve supported currencies and latest, historical, or date-range exchange rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a remote installer that has not been verified.

Mitigation: Review and install oo yourself before enabling the skill, and require approval before the agent runs either installer.

Risk: The CLI may change other agent skills through startup synchronization.

Mitigation: Consider whether to accept this behavior; the oo CLI command reference documents OO_SKILLS_SYNC_DISABLED as an option to disable startup synchronization.

## Reference(s):

- [CurrencyBeacon](https://currencybeacon.com)
- [CurrencyBeacon API documentation](https://currencybeacon.com/api-documentation)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-currencyscoop)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Currency and exchange-rate data as JSON, with concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected currency action and provider response.]

## Skill Version(s):

1.0.6 (source: skill metadata frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
