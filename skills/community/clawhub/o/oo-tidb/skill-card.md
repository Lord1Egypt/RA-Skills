## Description:

Use this skill to search and read TiDB Cloud data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform operators use the skill to inspect and query TiDB Cloud resources through an OOMOL-connected account. The agent checks each action's live schema and returns the results for the requested task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to execute a remote CLI installer without a separate approval step, and the installer and hosted connector implementation were not verified.

Mitigation: Review and separately approve the CLI installation; verify its source before running it.

Risk: Automatic agent-skill synchronization may introduce changes the user has not reviewed.

Mitigation: Review synchronization behavior and disable automatic synchronization if it is not needed.

Risk: TiDB account information returned by the connector may be sensitive, and broad connection permissions increase exposure.

Mitigation: Grant the OOMOL connection only the TiDB permissions needed and treat returned account information as sensitive.

## Reference(s):

- [TiDB Cloud API documentation](https://docs.pingcap.com/api/tidb-cloud-api-v1beta1/)
- [TiDB Cloud](https://www.pingcap.com/tidb/cloud/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-tidb)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON API results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas before calls; the documented actions are read-only.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
