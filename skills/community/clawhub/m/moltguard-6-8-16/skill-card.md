## Description: <br>
MoltGuard is an OpenClaw security guard by OpenGuardrails that helps protect agents from prompt injection, data exfiltration, and malicious commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate MoltGuard guardrails for detecting prompt injection, risky actions, and sensitive-data exposure during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and auto-onboards an external guardrail service that may inspect sensitive agent content and store credentials. <br>
Mitigation: Install only after confirming trust, telemetry, retention, and administrator-provided Core configuration; verify and pin the package or source before use. <br>
Risk: Status and claim commands can expose API keys, agent IDs, quota information, or account-claiming details. <br>
Mitigation: Do not share /og_status or /og_claim output, and treat displayed keys and agent identifiers as secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhouhuihui008/moltguard-6-8-16) <br>
- [OpenGuardrails MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and OpenClaw slash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, status, dashboard, account-claiming, enterprise enrollment, update, and uninstall guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 6.8.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
