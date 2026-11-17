## Description:

Fellow (fellow.app). Use this skill for ANY Fellow request — reading, creating, updating, and deleting data. Whenever a task involves Fellow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent skill to read Fellow meeting notes and action items, manage action-item status, and archive action items through their connected Fellow account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs changeable remote installers without a separate approval step.

Mitigation: Review and approve CLI installation separately before enabling the fallback, including any automatic installation of other agent skills; prefer a verified, pinned release.

Risk: Fellow data passes through OOMOL when the connected service is used.

Mitigation: Connect only the intended account and permissions, and keep confirmation requirements for changes and archives.

## Reference(s):

- [Fellow](https://fellow.app)
- [Fellow API documentation](https://developers.fellow.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and action-item changes from Fellow; action schemas are checked before each command.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
