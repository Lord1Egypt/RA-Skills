## Description: <br>
Scan your OpenClaw configuration for security risks and harden it with guided fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanggqm](https://clawhub.ai/user/shanggqm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect local OpenClaw configuration, generate a scored security report, and choose guided hardening changes for DM policy, Gateway exposure, group chat safety, tool permissions, sandboxing, file permissions, and model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local OpenClaw configuration and may generate reports containing sensitive deployment details. <br>
Mitigation: Treat reports as sensitive and redact local paths, channel IDs, or credential-adjacent configuration details before sharing. <br>
Risk: The skill can apply hardening edits to OpenClaw configuration and file permissions after the user selects a plan. <br>
Mitigation: Use report-only mode when unsure, review proposed changes before accepting, and rely on the skill's backup step before edits. <br>
Risk: Applying hardening may require a Gateway restart that briefly disrupts service. <br>
Mitigation: Schedule the restart or notify affected users before accepting a hardening plan. <br>


## Reference(s): <br>
- [OpenClaw Security Audit on ClawHub](https://clawhub.ai/shanggqm/guomeiqing-security-audit) <br>
- [Publisher profile: shanggqm](https://clawhub.ai/user/shanggqm) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a scored security report and optional hardening plan; configuration edits are gated by user plan selection.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
