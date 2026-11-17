## Description:

Use Bolna to inspect voice agents, executions, workspace information, and execution logs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to inspect Bolna voice agents, execution history, workspace account details, and raw execution logs through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run remote software whose exact contents are unverified, without a clear approval step.

Mitigation: Review setup first, install a verified oo CLI release yourself, require approval for installation changes, and review or disable automatic skill synchronization.

Risk: Connecting Bolna lets the agent retrieve workspace information and execution logs.

Mitigation: Connect the intended Bolna workspace and review retrieved information before sharing it.

## Reference(s):

- [Bolna API documentation](https://www.bolna.ai/docs/api-reference/introduction)
- [Bolna](https://www.bolna.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands and JSON request/response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bolna workspace records, agent details, execution history, and execution logs]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
