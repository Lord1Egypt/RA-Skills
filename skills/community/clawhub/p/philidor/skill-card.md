## Description:

DeFi vault intelligence for risk scores, yield comparison, portfolio analysis, and oracle monitoring across Morpho, Yearn, Aave, Beefy, and Spark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkoranges](https://clawhub.ai/user/zkoranges)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to research DeFi vaults, compare risk-adjusted yields, analyze wallet positions, and monitor vault safety signals across supported protocols and chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet analysis queries may associate submitted wallet addresses with Philidor service requests.

Mitigation: Avoid querying wallet addresses the user does not want shared with the Philidor service.

Risk: Vault recommendations can be misleading if treated as financial advice or based on APR alone.

Mitigation: Present results as research support, check risk breakdowns and recent incidents, and flag stale or incomplete data before recommending action.

Risk: The npm CLI dependency is not pinned by the skill metadata.

Mitigation: Review and trust the Philidor CLI package source before installation, and pin or mirror the dependency in controlled environments.

## Reference(s):

- [Philidor Website](https://philidor.io)
- [Philidor API Documentation](https://api.philidor.io/v1/docs)
- [Philidor Risk Methodology](https://philidor.io/risk)
- [ClawHub Skill Page](https://clawhub.ai/zkoranges/skills/philidor)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline Philidor CLI commands and JSON-oriented command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands can return JSON, table, or CSV; agent workflows should prefer explicit JSON output.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
