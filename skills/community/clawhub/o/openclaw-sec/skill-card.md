## Description: <br>
AI Agent Security Suite - Real-time protection against prompt injection, command injection, SSRF, path traversal, secrets exposure, and content policy violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaoloRollo](https://clawhub.ai/user/PaoloRollo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to validate agent prompts, commands, URLs, paths, and content for common attack patterns before or during OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent security hooks may inspect and log prompts and tool-call parameters. <br>
Mitigation: Review hook behavior, database path, retention settings, and notification endpoints before installation; reduce retention or disable logging where policy requires it. <br>
Risk: Automatic hook setup can change OpenClaw-wide behavior after installation. <br>
Mitigation: Review the postinstall hook behavior and confirm owner bypass and tool-call blocking settings match the intended environment before enabling the hooks. <br>


## Reference(s): <br>
- [Openclaw Sec on ClawHub](https://clawhub.ai/PaoloRollo/openclaw-sec) <br>
- [Hooks documentation](hooks/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-style text with security findings, severity, actions, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return allow, warn, log, or block actions depending on configured severity policy.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release metadata, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
