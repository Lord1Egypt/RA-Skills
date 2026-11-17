## Description:

Connects an agent to Kaonavi to read, create, update, and delete employee, personnel sheet, and login user data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Kaonavi can retrieve organizational and personnel records or prepare authorized changes to employee records, personnel sheets, and login users through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic dependency setup may execute downloaded installer code that has not been reviewed.

Mitigation: Review and install a verified CLI release before use; do not allow automatic script execution.

Risk: Automatic synchronization may change other agent skills.

Mitigation: Consider disabling additional skill synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the oo CLI command reference.

Risk: Kaonavi actions can change or delete employee, personnel sheet, and login user data.

Mitigation: Use a narrowly authorized Kaonavi connection and review each proposed change; confirm the exact effect before write or destructive actions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-kaonavi)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Kaonavi](https://www.kaonavi.jp/)
- [Kaonavi API documentation](https://developer.kaonavi.jp/api/v2.0/index.html)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples; Kaonavi action results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read data or change Kaonavi state; the skill requires confirmation before write and destructive actions.]

## Skill Version(s):

1.0.2 (source: skill frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
