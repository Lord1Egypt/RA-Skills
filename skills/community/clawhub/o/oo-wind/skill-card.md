## Description:

Access Wind market data, screening, and Alice research through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use Wind to query and screen market data, retrieve financial news and economic indicators, and run Wind Alice research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time CLI setup can execute remote code.

Mitigation: Review the setup path and use an explicitly approved, verified CLI release before installing.

Risk: Managed-skill synchronization can introduce broader agent changes than the skill explains.

Mitigation: Consider disabling managed-skill synchronization before invoking Wind.

Risk: Wind Alice research may continue consuming credits after the initial response.

Mitigation: Track ongoing research and resume the existing task rather than submitting it again.

## Reference(s):

- [Wind Alice API reference materials](https://github.com/Wind-Alice/AliceMarket/tree/main/skills/wind-mcp-skill/references)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Wind Alice marketplace](https://market.windalice.com/)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text, Files]

**Output Format:** [Structured financial data and research results as JSON or text, with report download URLs when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected Wind action; Alice research may continue after the initial response and consume credits.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
