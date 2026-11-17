## Description:

Google Docs: Append text to a document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to append plain text to an existing Google Docs document through the configured gws command-line account, after confirming the document ID and exact text with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill appends text to a Google Docs document through the configured gws account, so incorrect arguments can modify the wrong document or add unintended content.

Mitigation: Confirm the document ID, target account, and exact plain text with the user before execution.

## Reference(s):

- [Gws Docs Write on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-docs-write)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)
- [gws-shared auth and security rules](../gws-shared/SKILL.md)
- [gws-docs command family](../gws-docs/SKILL.md)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary, a Google Docs document ID, and plain text to append; the action writes to the target document.]

## Skill Version(s):

1.0.12 (source: server release evidence; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
