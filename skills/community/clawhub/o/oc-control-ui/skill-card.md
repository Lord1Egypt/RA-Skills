## Description:

Operate and troubleshoot the OpenClaw Control UI: navigate connected clients, organize sessions, build session dashboards, and handle direct or Tailscale-hosted Gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to navigate connected Control UI clients, organize sessions, build and verify session dashboards, and troubleshoot direct or remotely hosted Gateways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated security review was partial because two local references could not be resolved.

Mitigation: Review the skill instructions and verify the referenced material before installing or applying its guidance.

Risk: Remote proxy or sandbox misconfiguration can expose authenticated UI traffic or leave dashboard widgets unreachable.

Mitigation: Keep the authenticated Control UI and unprivileged widget sandbox on separate origins, route the sandbox only to its listener, and verify each proxy hop’s protocol and authentication handling.

Risk: Sharing or logging a short-lived dashboard bootstrap URL can expose its credentials.

Mitigation: Do not paste or log bootstrap credentials; use the local bootstrap flow only in the intended browser.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/oc-control-ui)
- [Dashboard operations](references/dashboards.md)
- [Control UI hosting paths](references/hosting.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with UI operations, code examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dashboard layout guidance, custom HTML/SVG widget content, and remote-hosting troubleshooting steps.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
