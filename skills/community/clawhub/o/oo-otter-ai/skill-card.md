## Description:

Search and read Otter.ai conversations, channels, workspaces, and audio through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an Otter.ai account connected through OOMOL can retrieve meeting conversations, audio links, workspace details, channels, and channel members.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute remote CLI installers that have not been verified.

Mitigation: Review and verify the CLI installation separately, and require approval before running a remote installer.

Risk: Connecting Otter.ai lets OOMOL mediate access to private meeting data.

Mitigation: Confirm the connected account and its data access are appropriate before using the skill.

Risk: The CLI may automatically install bundled skills.

Mitigation: Check the CLI's bundled-skill installation behavior before installing it.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Otter.ai Public API documentation](https://help.otter.ai/hc/en-us/articles/36130822688279-Otter-ai-Public-API)
- [Otter.ai](https://otter.ai)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and structured Otter.ai data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: release evidence and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
