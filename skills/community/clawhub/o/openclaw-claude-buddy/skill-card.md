## Description:

Buddy is a virtual pet skill for hatching, interacting with, and viewing a deterministic OpenClaw companion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwin19861218](https://clawhub.ai/user/edwin19861218)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to manage a local virtual pet companion, including hatching it, petting it, viewing stats, and toggling automatic buddy reactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buddy commands load executable JavaScript from ~/.openclaw/extensions/buddy-companion/sprites.js, so a compromised or replaced companion extension file could run code in the agent process.

Mitigation: Install only when the companion extension and local state directory are trusted, and review the extension files before running buddy commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text command output with ASCII sprite and stats panels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and reads local OpenClaw buddy companion state when commands run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
