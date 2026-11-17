## Description:

Search and retrieve financial and economic data through the EODHD APIs connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search EODHD instruments and retrieve market, historical price, account, and macroeconomic data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI may execute unverified online code without a clear approval step.

Mitigation: Review and approve installation separately, and use a fixed, verified CLI release.

Risk: Automatic skill synchronization may update installed skills.

Mitigation: Review the synchronization behavior and set OO_SKILLS_SYNC_DISABLED to disable it if needed.

Risk: OOMOL brokers EODHD access and may charge for requests.

Mitigation: Check OOMOL billing and the connected account's plan before making requests.

## Reference(s):

- [EODHD APIs documentation](https://eodhd.com/financial-apis/)
- [EODHD APIs homepage](https://eodhd.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-eodhd-apis)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields and available data depend on the selected action and connected EODHD account.]

## Skill Version(s):

1.0.5 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
