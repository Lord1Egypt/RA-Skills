## Description: <br>
Portkey-inspired guardrails for OpenClaw: 5 configurable rules that block prompt injection, redact PII, flag off-scope responses, enforce agent budgets, and warn on context length. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to apply configurable guardrails to inbound and outbound agent messages, including prompt-injection blocking, PII redaction, off-scope flagging, budget enforcement, context-length warnings, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release as suspicious because the active hook can inspect, block, and rewrite messages while loading local guardrail implementation code. <br>
Mitigation: Review the implementation before installing, package the referenced guardrails code with the release, and test block and redact behavior on non-production agents. <br>
Risk: Audit logs and optional cache behavior may create local data-retention concerns. <br>
Mitigation: Confirm where audit and cache data are stored, set retention expectations before enabling the hook, and disable or scope optional cache behavior where it is not needed. <br>
Risk: The hook is designed to fail open if the guardrails module cannot be loaded. <br>
Mitigation: Monitor hook load failures and include startup checks so operators know when guardrails are not active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/portkey-guardrails) <br>
- [Portkey open-source LLM gateway](https://github.com/Portkey-AI/gateway) <br>
- [Agent configuration schema](artifact/rules/config-schema.yaml) <br>
- [Hook metadata](artifact/hook/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [OpenClaw hook decisions, redacted message text, markdown audit entries, YAML configuration, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs offline by default; local Ollama is optional for semantic-cache behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
