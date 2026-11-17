## Description:

Operate Hoop through an OOMOL-connected account to search and read data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Hoop users and developers can use this skill to inspect the connected profile and list Hoop connections or sessions. It fetches each action's live schema before sending a read request through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run an online CLI installer whose behavior is outside the verified artifact.

Mitigation: Review and install a verified oo CLI release yourself before enabling the skill.

Risk: Connecting Hoop entrusts OOMOL with access to the connected account.

Mitigation: Review the account access and automatic skill synchronization settings before connecting.

## Reference(s):

- [Hoop homepage](https://hoop.dev)
- [Hoop API documentation](https://hoop.dev/docs/api-reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Hoop skill release](https://clawhub.ai/oomol/skills/oo-hoop)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Structured JSON connector results with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only profile, connection, and session data returned by Hoop.]

## Skill Version(s):

1.0.4 (source: frontmatter; server-resolved release 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
