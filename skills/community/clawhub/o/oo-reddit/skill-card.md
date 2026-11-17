## Description:

Reddit (reddit.com). Use this skill for ANY Reddit request — reading, creating, updating, and deleting data. Whenever a task involves Reddit, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Reddit through an OOMOL-connected account can read posts and comments, search Reddit, and manage their own posts and comments. Confirm the exact content before creating, editing, or deleting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded software without separate approval or integrity verification.

Mitigation: Preinstall a reviewed, pinned CLI version, check whether it adds other agent skills, and require approval before running any downloaded installer.

Risk: Creating, editing, or deleting Reddit content changes the authenticated account's data.

Mitigation: Keep the skill's explicit confirmations for posting, editing, and deleting, and confirm the exact payload and effect before execution.

## Reference(s):

- [Reddit API documentation](https://www.reddit.com/dev/api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON action responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions and returned data depend on the connected Reddit account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
