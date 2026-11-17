## Description:

Minerstat (minerstat.com). Use this skill for ANY Minerstat request — searching and reading data. Whenever a task involves Minerstat, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Minerstat can retrieve coin profitability and market data, GPU and ASIC benchmarks, and mining pool information through their connected Minerstat account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute an online CLI installer without a clear approval step.

Mitigation: Review and install a verified CLI release yourself before allowing agent use, and check its agent-skill synchronization settings.

Risk: Connecting Minerstat entrusts its API credential to OOMOL.

Mitigation: Connect only if you are comfortable entrusting the Minerstat API credential to OOMOL.

## Reference(s):

- [Minerstat homepage](https://minerstat.com/)
- [Minerstat API documentation](https://api.minerstat.com/docs-coins)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-minerstat)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [Minerstat data returned as JSON, with text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented results for coins, hardware, and pools; setup guidance may include CLI installation commands.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
