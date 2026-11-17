## Description:

Helps open a locally hosted agent-skeleton assistant at localhost:3000 and troubleshoot startup or port issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All rights reserved (skill documentation); MIT (.py code only)

## Use Case:

Developers and local assistant users use this skill to check whether their agent-skeleton server is running, open its local page, or diagnose why the page does not load.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting the local server may create files or leave a background process running.

Mitigation: Confirm the project path and planned startup action with the user before running node server.js.

Risk: Troubleshooting may change network exposure, system settings, or dependencies.

Mitigation: Keep the page on localhost and request explicit approval before firewall, hosts, dependency, or public-exposure changes.

## Reference(s):

- [local-agent-open on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/local-agent-open)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Localhost access only; starting the server requires user confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
