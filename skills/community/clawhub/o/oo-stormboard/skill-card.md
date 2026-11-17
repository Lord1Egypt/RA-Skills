## Description:

Use this skill to search and read Stormboard data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the agent to inspect Stormboard profiles, storms, ideas, participants, tags, connectors, and templates through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software without a user approval step, and its dependency may install additional agent skills.

Mitigation: Review and approve the oo installation separately before use; check its startup synchronization controls and ensure you accept OOMOL handling the Stormboard connection and requests.

## Reference(s):

- [Stormboard API documentation](https://api.stormboard.com/docs)
- [Stormboard](https://stormboard.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Stormboard account data from the listed actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
