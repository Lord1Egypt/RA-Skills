## Description:

OpenBuddy is a terminal virtual pet system for hatching, raising, and interacting with an ASCII pet companion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wltgithub](https://clawhub.ai/user/wltgithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use OpenBuddy to add a terminal-based virtual pet companion to coding sessions, including hatching a pet, viewing its status card, petting it, muting or hiding it, and sending simple talk messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a local pet-state file under ~/.openbuddy by default.

Mitigation: Use OPENBUDDY_DIR to choose a different storage location when the default home-directory path is not appropriate.

Risk: OPENBUDDY_USER_ID influences deterministic pet generation and could contain sensitive personal identifiers if set carelessly.

Mitigation: Use a non-sensitive stable alias for OPENBUDDY_USER_ID when overriding the default user identifier.

## Reference(s):

- [OpenBuddy ClawHub listing](https://clawhub.ai/wltgithub/skills/openbuddy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js and stores local pet state in ~/.openbuddy/buddy-soul.json by default; OPENBUDDY_DIR can redirect storage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
