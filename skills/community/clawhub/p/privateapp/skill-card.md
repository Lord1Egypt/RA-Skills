## Description:

Personal PWA dashboard server for installing, operating, building, extending, and configuring a private FastAPI and React home-server app with plugin apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:

MIT

## Use Case:

Developers and home-server operators use this skill to install and run PrivateApp, manage its service, build frontend assets, add plugin apps, configure push notifications, and operate private system monitoring and file browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default network exposure can make the dashboard reachable beyond the intended private environment.

Mitigation: Run only behind a trusted private network, bind to localhost unless strong network controls are in place, and add authentication before exposing it to any network.

Risk: The file browser can expose the user's home directory by default.

Mitigation: Change the file browser root away from the home directory and restrict it to the smallest directory needed.

Risk: Unauthenticated restart, shutdown, and plugin-discovery management endpoints can affect the host system.

Mitigation: Remove, disable, or lock down restart, shutdown, and plugin-discovery management endpoints before network exposure.

Risk: Installation and frontend build dependencies may introduce supply-chain exposure.

Mitigation: Upgrade frontend build dependencies and avoid the optional pipe-to-shell Tailscale install path unless it has been independently trusted and verified.

## Reference(s):

- [PrivateApp ClawHub Skill Page](https://clawhub.ai/camopel/skills/privateapp)
- [PrivateApp README](artifact/README.md)
- [PrivateApp Skill Instructions](artifact/SKILL.md)
- [Tailscale Download](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local installation steps, service management commands, frontend build commands, plugin scaffolding guidance, and push notification configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
