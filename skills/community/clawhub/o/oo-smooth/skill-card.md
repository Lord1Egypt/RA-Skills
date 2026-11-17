## Description:

Smooth (smooth.sh). Use this skill for ANY Smooth request — reading, creating, updating, and deleting data. Whenever a task involves Smooth, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to read and manage Smooth data through a connected account, including submitting browser tasks and managing reusable profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup can execute a remote installer, and the CLI may install additional agent skills at startup.

Mitigation: Review the installer and CLI release before installation; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Submitted browser tasks can change or delete data on visited sites, and reusable profiles retain cookies and authentication across tasks.

Mitigation: Require approval for browser tasks and profile changes, review each task's intended effects, and consider which account sessions a profile retains.

## Reference(s):

- [Smooth homepage](https://smooth.sh)
- [Smooth API documentation](https://docs.smooth.sh/api-reference/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo shell commands, JSON request payloads, and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include task data and an execution ID.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
