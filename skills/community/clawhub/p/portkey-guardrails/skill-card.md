## Description:

Portkey-inspired guardrails for OpenClaw that block prompt injection, redact PII, flag off-scope responses, enforce agent budgets, and warn on context length as a workspace hook without an external service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add configurable guardrails to OpenClaw message flows, including prompt-injection blocking, outbound PII redaction, topic flagging, budget enforcement, context-length warnings, per-agent configuration, and audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed hook loads an external workspace guardrails implementation that is not included in the package.

Mitigation: Install only in workspaces where the external implementation path is trusted, controlled, and reviewed before enabling the hook.

Risk: Off-scope filtering is audit-only and can allow flagged content to continue through the message flow.

Mitigation: Treat G-03 findings as monitoring signals unless the workspace explicitly configures stricter handling.

Risk: Budget enforcement reads per-agent budget files based on the resolved agent identifier.

Mitigation: Validate agent identifiers and restrict workspace file permissions before relying on budget-based blocking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/portkey-guardrails)
- [Publisher Profile](https://clawhub.ai/user/nissan)
- [Portkey Open Source LLM Gateway](https://github.com/Portkey-AI/gateway)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Hook decisions, redacted message text, Markdown audit entries, YAML configuration, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs without outbound network access; Ollama is optional for semantic cache behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, CHANGELOG released 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
