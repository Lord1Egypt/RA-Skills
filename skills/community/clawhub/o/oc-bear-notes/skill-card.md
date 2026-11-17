## Description:

Create, search, and manage Bear notes via grizzly CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

macOS Bear users can use the skill to create, read, append to, search, and organize notes through grizzly. Bear must be installed and running, and some actions require a Bear API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because a referenced local path was missing.

Mitigation: Locate and review any referenced local files before relying on behavior that depends on them.

Risk: Commands can create or change Bear notes and tags.

Mitigation: Review note content, title, tags, and target note ID before running write commands.

Risk: Some operations use a Bear API token stored in a local file.

Mitigation: Keep the token file private and avoid including the token in shared commands or output.

## Reference(s):

- [Bear](https://bear.app)
- [Bear Notes on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-bear-notes)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands; grizzly callback operations can return JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Bear on macOS; some operations require a Bear API token.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
