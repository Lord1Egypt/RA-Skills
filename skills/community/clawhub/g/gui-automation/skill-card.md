## Description:

Control the desktop via the CUA computer server API running on port 8000.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarinali](https://clawhub.ai/user/sarinali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to let an agent inspect and control a local desktop through a CUA server for GUI workflows such as screenshots, clicks, typing, application launch, browser navigation, and form filling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact desktop control through an unauthenticated local control API.

Mitigation: Install only when desktop control is intentional, bind the server explicitly to 127.0.0.1, run it in a monitored foreground session, and stop it when finished.

Risk: The skill depends on third-party server installation steps that may be unpinned.

Mitigation: Use a pinned and reviewed server version in an isolated environment, and verify the package publisher and version before running it.

Risk: Exposing the server beyond localhost or changing system permissions can broaden access to keyboard, mouse, screenshot, and application-control capabilities.

Mitigation: Avoid network exposure, background operation, and sudo group changes unless necessary and reviewed for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarinali/skills/gui-automation)
- [CUA computer server source](https://github.com/trycua/cua-computer-server)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local CUA server, commonly bound to 127.0.0.1 on port 8000.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
