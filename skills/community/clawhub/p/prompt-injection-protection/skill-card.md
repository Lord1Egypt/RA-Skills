## Description:

Protects against prompt injection attacks by sanitizing, validating, and securely processing untrusted external content from websites, emails, and documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackworm](https://clawhub.ai/user/blackworm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to screen untrusted web, email, document, command, and file-operation content for prompt-injection patterns before passing it into sensitive workflows. It provides sanitization, validation, alerting, context isolation, and pre-check helpers for safer downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security protections may fail open in non-strict processing paths.

Mitigation: Use strictMode for untrusted content and treat any secured or isSafe flag as advisory until callers verify the returned threat details.

Risk: The skill auto-loads and starts background update behavior by default.

Mitigation: Disable or tightly control auto-loading and auto-updates before using the skill in sensitive web, email, document, command, or file workflows.

Risk: Persistent auto-learning can retain patterns derived from untrusted content.

Mitigation: Review and manage learned-threat storage, disable learning where persistence is not acceptable, and clear learned state during incident response or environment resets.

Risk: Server security evidence reports a suspicious verdict for this release.

Mitigation: Install only after implementation review and avoid automatic use in sensitive workflows until the fail-open and persistence issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackworm/skills/prompt-injection-protection)
- [ClawHub publisher profile](https://clawhub.ai/user/blackworm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, JSON-like result objects, security alerts, and command or file-operation pre-check responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit sanitized content, threat classifications, severity values, alert callback payloads, learned-threat state, and safe context wrappers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
