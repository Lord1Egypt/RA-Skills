## Description: <br>
Better Stack (betterstack.com). Use this skill for ANY Better Stack request — reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and incident responders use this skill to read and manage Better Stack incidents, comments, metadata, and escalation workflows through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident-management actions can affect alerting, escalation, or on-call routing. <br>
Mitigation: Require explicit user approval before creating, acknowledging, or escalating incidents, and review payloads before execution. <br>
Risk: The skill requires access to Better Stack through an OOMOL-connected account. <br>
Mitigation: Install only where Better Stack account permissions are appropriate for the intended operational scope. <br>


## Reference(s): <br>
- [ClawHub Better Stack Skill](https://clawhub.ai/oomol/oo-better-stack) <br>
- [Better Stack Homepage](https://betterstack.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Better Stack Icon](https://static.oomol.com/logo/third-party/Better%20Stack.svg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; Better Stack credentials are required through the connected OOMOL account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
