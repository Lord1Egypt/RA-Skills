## Description:

Search and read CoinMarketCal market calendar data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to search CoinMarketCal for coins, confirmed events, event categories, general events, or ranked events, and read the returned market calendar data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code that has not been verified, and the skill's remote installer contents remain unverified.

Mitigation: Review the CLI and installer before installation, and explicitly approve local software changes.

Risk: Using the connected account involves CoinMarketCal credentials and may incur OOMOL or provider billing.

Mitigation: Use a trusted OOMOL account, review the CoinMarketCal connection and billing terms, and stop on billing errors until the responsible account is checked.

Risk: Automatic agent-skill changes may affect the local environment.

Mitigation: Review skill changes; the documented synchronization control is OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [CoinMarketCal developer documentation](https://coinmarketcal.com/developer/docs)
- [OOMOL CLI commands reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [CoinMarketCal ClawHub release](https://clawhub.ai/oomol/skills/oo-coinmarketcal)

## Skill Output:

**Output Type(s):** [Structured data, Guidance]

**Output Format:** [JSON data returned by CoinMarketCal, with usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market calendar results; the connector returns data and execution metadata.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
