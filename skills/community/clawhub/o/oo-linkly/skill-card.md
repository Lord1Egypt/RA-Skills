## Description:

Linkly (linklyhq.com). Use this skill for ANY Linkly request — reading, creating, updating, and deleting data. Whenever a task involves Linkly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read and manage Linkly workspaces and short links through their connected OOMOL account. It guides an agent to inspect each action's schema, then issue the corresponding request, with confirmation required for changes and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the user to run a remote installation script and may affect other agent skills through automatic synchronization.

Mitigation: Review the setup behavior first, install a verified oo CLI version separately, and review or disable automatic skill synchronization.

Risk: Linkly requests are processed through OOMOL, and write or delete actions can change user data.

Mitigation: Understand that OOMOL processes requests and retain the skill's confirmation requirements for changes and deletion.

## Reference(s):

- [Linkly API documentation](https://linklyhq.com/url-shortener-api-reference)
- [Linkly homepage](https://linklyhq.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON responses and shell commands executed through the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create, update, or delete Linkly data require user confirmation.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
