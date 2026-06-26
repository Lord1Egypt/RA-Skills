## Description: <br>
Host security hardening and risk-tolerance configuration for OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to audit and harden hosts running OpenClaw, plan firewall, SSH, update, and service changes, and configure periodic health checks with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Host hardening guidance can affect firewall, SSH, services, packages, update policy, scheduled tasks, or access to sensitive files. <br>
Mitigation: Review each proposed command before approval; the skill requires explicit approval for state-changing actions and emphasizes staged, reversible changes with rollback planning. <br>
Risk: Remote access changes can lock users out of a host. <br>
Mitigation: Confirm how the user connects before modifying remote access settings and preserve access paths during remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-healthcheck) <br>
- [Publisher profile](https://clawhub.ai/user/mohdalhashemi98-hue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit approval before state-changing host or OpenClaw operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
