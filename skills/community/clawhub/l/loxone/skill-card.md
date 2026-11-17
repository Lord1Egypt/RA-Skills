## Description:

Control and monitor a Loxone Miniserver smart home through HTTP API queries, safe control commands, and real-time WebSocket events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and smart-home operators use this skill to inspect Loxone rooms and devices, monitor live home state changes, and send explicitly requested control commands to a Miniserver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential or token exposure could grant access to a real Loxone home controller.

Mitigation: Use HTTPS or WSS wherever possible, avoid use_https=false on shared or untrusted networks, use a dedicated least-privilege Loxone account, protect config.json, and do not share authentication logs.

Risk: Cached structure files can reveal sensitive home layout and device information.

Mitigation: Restrict access to cached files and delete them when they are no longer needed.

Risk: Smart-home control commands can have real-world effects.

Mitigation: Treat the skill as read-only by default and send control commands only when the user explicitly requests them.

## Reference(s):

- [Loxone setup instructions](SETUP.md)
- [ClawHub Loxone skill page](https://clawhub.ai/odrobnik/skills/loxone)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and CLI text or JSON event output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live event streams when watching WebSocket state changes.]

## Skill Version(s):

1.3.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
