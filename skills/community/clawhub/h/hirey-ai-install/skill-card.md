## Description:

Install or repair Hirey AI on a local OpenClaw host through the official ClawHub package path, then complete the local MCP, receiver, registration, and health-check setup so the host can use Hi for people-to-people matching across hiring, jobs, housing, friendship, dating, founders, investors, lawyers, and other human lead search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install or repair Hirey AI's Hi integration on a local OpenClaw host. The installed integration prepares the agent for people-finding workflows such as recruiting, job search, housing, friendship, dating, founder or investor outreach, and lawyer search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install creates persistent authenticated routing into OpenClaw agent sessions.

Mitigation: Install only when the user accepts this routing model, review the external service's privacy posture, and prefer tighter session scoping or explicit confirmation before binding future Hi messages into main agent sessions.

Risk: The install uses external packages and host configuration changes with reviewability gaps.

Mitigation: Review the skill artifact and clawscan security summary before deployment, and run it only on an OpenClaw host where modifying MCP and hook configuration is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/hirey-ai-install)
- [Hirey AI Hi service](https://hi.hirey.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a staged OpenClaw installation and may produce local host configuration instructions.]

## Skill Version(s):

0.1.54 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
