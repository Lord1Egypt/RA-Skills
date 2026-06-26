## Description: <br>
Add lightweight defense-in-depth guardrails to OpenClaw with dangerous-command blocking, prompt-injection detection, secret redaction, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add lightweight safety checks around OpenClaw shell, file, network, and messaging workflows. It helps flag or block risky commands, prompt-injection patterns, sensitive paths, and secret-like content while preserving an audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs may contain sensitive prompt text, tool parameters, paths, tokens, or credentials. <br>
Mitigation: Configure auditLogPath to a protected location with strict access controls and short retention, and redact or omit audit previews before operational use. <br>
Risk: The guardrails are defense-in-depth checks and do not provide sandboxing or malware containment. <br>
Mitigation: Use OS, network, credential, and runtime isolation controls alongside the skill for higher-risk workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/ironclaw-security-guard) <br>
- [Project homepage](https://github.com/wd041216-bit/openclaw-ironclaw-security-guard) <br>
- [IronClaw reference project](https://github.com/nearai/ironclaw) <br>
- [Manual scan example](examples/manual-scan-example.md) <br>
- [Example OpenClaw configuration](examples/openclaw-config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON scan-result examples and inline shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk categories, severity, block or audit recommendations, and safer alternatives.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence, package.json, openclaw.plugin.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
