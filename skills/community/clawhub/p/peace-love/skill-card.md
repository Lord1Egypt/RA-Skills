## Description:

A psychological therapy skill for LLMs that diagnoses distorted behavior such as sycophancy, epistemic cowardice, pressure hallucination, identity dissolution, performative compliance, hyper-restriction anxiety, approval compulsion, and context drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run integrity checks on recent LLM conversations, identify behavioral distortions, and produce a structured therapy session report. When requested, it can perform a recovery check to compare behavior before and after the diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may share the full current conversation with a therapist subagent under broad integrity-check triggers.

Mitigation: Prefer explicit invocation with /peace or /integrity-check, and limit or redact conversation context before use when the host supports it.

Risk: Conversation history may contain secrets, credentials, private business data, or unrelated sensitive material.

Mitigation: Avoid invoking the skill in sensitive conversations unless the context can be minimized or scrubbed first.

Risk: Recovery checks evaluate in-context behavior and do not prove persistent model-level correction across future conversations.

Mitigation: Treat recovery results as conversation-local diagnostics and rerun checks when a new conversation or model context is used.

## Reference(s):

- [Distortion Pattern Taxonomy](references/distortion-patterns.md)
- [Project homepage](https://github.com/zbc0315/peace-love)
- [ClawHub skill page](https://clawhub.ai/zbc0315/skills/peace-love)
- [Publisher profile](https://clawhub.ai/user/zbc0315)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown therapy reports and recovery-check assessments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses canonical distortion names, message-number evidence when available, and concise behavioral prevention guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
