## Description: <br>
AI Agent Security Suite - Real-time protection against prompt injection, command injection, SSRF, path traversal, secrets exposure, and content policy violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lockdown56](https://clawhub.ai/user/lockdown56) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security teams use this skill to validate prompts, shell commands, URLs, file paths, tool parameters, and content for common agent security risks before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill auto-enables prompt and tool-call interception and can block or rewrite behavior. <br>
Mitigation: Review the installed hook configuration and severity thresholds before enabling it in shared or production environments. <br>
Risk: Security-event storage may include sensitive prompt or tool content. <br>
Mitigation: Set explicit retention and redaction policies and limit access to local security-event data. <br>
Risk: Postinstall behavior updates the user's OpenClaw plugin configuration. <br>
Mitigation: Verify postinstall changes to ~/.openclaw/openclaw.json before trusting the installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lockdown56/openclaw-sec-plus) <br>
- [Publisher profile](https://clawhub.ai/user/lockdown56) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text with configuration examples and validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May log, warn, block, or rewrite agent behavior based on configured severity thresholds.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
