## Description: <br>
Enables two OpenClaw instances to monitor each other with heartbeats, run health checks, diagnose failures, and issue repair actions for high-availability operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers use this skill to configure paired OpenClaw nodes that exchange health signals, report local resource and process status, diagnose peer failures, and perform administrator-level restart actions when repair is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes remote repair controls without built-in authentication or confirmation. <br>
Mitigation: Install only in a private, firewalled environment, restrict port 9528 to trusted peer IPs, and treat restart actions as administrator-only until authentication, request validation, audit logging, and explicit approval are added. <br>
Risk: The release package evidence includes an exposed ClawHub token in publication instructions. <br>
Mitigation: Remove the token from release materials and rotate it before installation or reuse. <br>
Risk: Remote host and port configuration can drive network checks and repair requests toward unintended systems. <br>
Mitigation: Use trusted configuration values, validate peer addresses before deployment, and keep the service isolated from untrusted networks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rfdiosuao/openclaw-mutual-repair) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with status summaries, diagnostic findings, configuration snippets, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local HTTP heartbeat and repair listener and may execute local health-check or restart commands when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
