## Description:

Search Marketstack and retrieve market data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search Marketstack listings and retrieve end-of-day prices, ticker profiles, currencies, and exchange data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installer and automatic skill synchronization can execute unverified software and change persistent agent skills.

Mitigation: Review the installer and intended version before installation, inspect automatic skill changes, and consider the documented OO_SKILLS_SYNC_DISABLED control.

Risk: Marketstack queries and authentication use OOMOL, so account permissions and billing affect use.

Mitigation: Review OOMOL account permissions and billing before connecting.

## Reference(s):

- [Marketstack](https://marketstack.com)
- [Marketstack API documentation](https://docs.apilayer.com/marketstack/docs/marketstack-api-v2-v-2-0-0)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Marketstack ClawHub release](https://clawhub.ai/oomol/skills/oo-marketstack)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
