## Description:

Add lightweight defense-in-depth guardrails to OpenClaw with dangerous-command blocking, prompt-injection detection, secret redaction, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add lightweight guardrails to OpenClaw runtimes that inspect tool calls, detect prompt-injection patterns, redact secrets, and keep audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs can persist sensitive message and tool contents locally, including data the skill is intended to protect.

Mitigation: Use a private audit path with restrictive permissions and prefer deployments that redact audit previews centrally before use with sensitive prompts, tool parameters, or outgoing messages.

Risk: This skill adds defense-in-depth checks but does not provide container isolation, sandboxing, or full malware containment.

Mitigation: Keep OS, credential, network, and runtime controls in place, and treat the skill as a guardrail rather than a security boundary.

Risk: Heuristic command, path, prompt-injection, and secret-detection rules can produce false positives or miss novel patterns.

Mitigation: Review audit entries before overriding blocked calls and test local allowlists, protected paths, and blocked-command patterns before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/ironclaw-security-guard)
- [Project homepage](https://github.com/wd041216-bit/openclaw-ironclaw-security-guard)
- [README](README.md)
- [Security policy](SECURITY.md)
- [Manual scan example](examples/manual-scan-example.md)
- [OpenClaw plugin manifest](openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON scan results and inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted previews, finding categories, severity labels, safer alternatives, and block recommendations.]

## Skill Version(s):

0.2.0 (source: server release metadata, package.json, skill.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
