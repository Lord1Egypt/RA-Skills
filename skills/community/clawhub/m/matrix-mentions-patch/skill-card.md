## Description:

Fix OpenClaw Matrix plugin mention detection by guiding users to pass the agent ID to buildMentionRegexes when Matrix group-room @mentions are not detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose and apply a manual OpenClaw Matrix extension patch when a bot fails to respond to required @mentions in Matrix group rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance changes local OpenClaw Matrix extension code and restarts the gateway.

Mitigation: Confirm the extension path, review the exact edit, and keep a backup before restarting the gateway.

Risk: Using the wrong agent ID can leave mention detection misconfigured.

Mitigation: Replace the example agent ID with the actual configured agent ID before applying the patch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biociao/skills/matrix-mentions-patch)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a local source edit and gateway restart; no executable code is bundled.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
