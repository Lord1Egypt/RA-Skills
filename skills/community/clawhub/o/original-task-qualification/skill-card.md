## Description:

Qualify one public SameDayDesk original task with the included correspondence client and read that private attempt; this is not delivery, acceptance, or payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can assess whether one public original task fits SameDayDesk correspondence, explicitly submit it for qualification, and read the resulting private attempt. Qualification does not imply delivery, acceptance, or payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a task contacts SameDayDesk and stores a private attempt containing a generated registration secret.

Mitigation: Submit only intentionally; keep cache and private directories separate and protect the private directory.

Risk: An admin or operator token could be exposed if provided to the skill.

Mitigation: Do not provide or expose admin or operator tokens to this skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/epistemedeus/skills/original-task-qualification)
- [Included client manifest](references/included-client.json)
- [Client and discovery pins](references/pins.json)
- [SameDayDesk public discovery descriptor](https://samedaydesk.com/discovery/original-task-correspondence.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance and shell commands; commands return JSON observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22 or later and tar. Offline describe and map are distinct from explicit online submit and read actions.]

## Skill Version(s):

0.2.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
