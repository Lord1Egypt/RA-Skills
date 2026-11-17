## Description:

Animated pixel art desktop pet that roams the screen as an always-on-top Electron overlay, avoids the cursor and active windows, and responds to agent state changes through a local HTTP API on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samskrta](https://clawhub.ai/user/samskrta)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to run a macOS desktop companion that reflects agent activity with animated states such as talking, working, thinking, sleeping, and walking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent macOS Electron app with a local API.

Mitigation: Review before installing, make auto-start an explicit user choice, and confirm the LaunchAgent behavior is acceptable for the target environment.

Risk: The server security review reports unsafe local control paths that could let another local process run code as the user.

Mitigation: Prefer a version that removes executeJavaScript, renders bubble text safely, disables Node integration, and authenticates or replaces the local API.

Risk: Dependencies are installed without a lockfile.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [Mu Pet ClawHub skill page](https://clawhub.ai/samskrta/skills/mu-pet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation guidance and agent integration examples for a macOS Electron desktop overlay.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
