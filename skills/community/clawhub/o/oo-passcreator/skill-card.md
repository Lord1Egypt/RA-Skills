## Description:

Use Passcreator for reading, creating, and updating data; whenever a task involves Passcreator, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Passcreator templates and passes, search pass records, and create wallet passes through a connected Passcreator account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can execute remote installation code without separate user approval.

Mitigation: Review the setup fallback, prefer installing a verified CLI yourself, and require approval before software installation or changes to other agent skills.

Risk: Creating a wallet pass changes Passcreator account data.

Mitigation: Confirm the exact payload and effect with the user before running the create_pass write action.

## Reference(s):

- [Passcreator homepage](https://www.passcreator.com/)
- [Passcreator API documentation](https://developer.passcreator.com/en)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-passcreator)

## Skill Output:

**Output Type(s):** [API calls, JSON data, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands with inline JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Passcreator read results or wallet-pass creation results; write actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
