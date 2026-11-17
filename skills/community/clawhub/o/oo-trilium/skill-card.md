## Description:

Connects an agent to TriliumNext Notes to search, read, create, update, and delete notes, note content, attributes, branches, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using TriliumNext Notes can ask an agent to search and manage their notes through their connected OOMOL account. The skill describes which actions read data and which change or delete it, and requires confirmation before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run remote dependency installers without a separate approval step.

Mitigation: Review dependency setup before installing, use a reviewed fixed oo CLI release, require approval before host changes, and disable unwanted skill synchronization. Confirm note changes before running write or destructive actions.

## Reference(s):

- [TriliumNext Notes](https://triliumnotes.org)
- [TriliumNext ETAPI documentation](https://docs.triliumnotes.org/user-guide/advanced-usage/etapi)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-trilium)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON input payloads and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill distinguishes read actions from writes and destructive actions; those changes require user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
