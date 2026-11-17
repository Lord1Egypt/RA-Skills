## Description:

Provides access to Jin10 data for search and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can ask an agent to search and retrieve Jin10 news, flash updates, economic calendar items, quotes, and minute-level market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote code and make persistent changes to the agent's available skills.

Mitigation: Review setup before enabling the skill, install a verified and pinned CLI separately, and approve environment changes explicitly.

Risk: Use may rely on OOMOL account permissions and incur service costs.

Mitigation: Check the connected account's permissions and applicable service costs before use.

## Reference(s):

- [Jin10](https://www.jin10.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Jin10 skill release](https://clawhub.ai/oomol/skills/oo-jin10)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Jin10 data returned as JSON and summarized in agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested Jin10 action and available account access.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
