## Description:

Workast (workast.com). Use this skill for ANY Workast request — reading, creating, and updating data. Whenever a task involves Workast, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Workast users can use the skill to find spaces and read task or account details, then create, update, or complete tasks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs unverified installation scripts and can install and synchronize skills without a separate approval step.

Mitigation: Before enabling setup, review and explicitly approve the CLI installation; prefer a reviewed, pinned release.

Risk: Creating, updating, or completing tasks changes Workast data.

Mitigation: Review the exact action and payload with the user and get confirmation before running a write action.

## Reference(s):

- [Workast](https://www.workast.com/)
- [Workast API documentation](https://developers.workast.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Natural-language guidance, shell commands, JSON connector payloads, and Workast action results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads return Workast data; task creation, updates, and completion change Workast state.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
