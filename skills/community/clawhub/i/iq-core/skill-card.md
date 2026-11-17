## Description:

Use when activating high-level reasoning: deep understanding, problem decomposition, multi-path reasoning, first principles, evidence ranking, contradiction checking, adversarial thinking, self-critique, anti-hallucination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to apply structured reasoning, evidence ranking, contradiction checks, and self-critique before answering complex or uncertain tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional reasoning log helper can persist task details locally, which could include secrets or sensitive personal data if the user supplies them.

Mitigation: Do not place secrets or sensitive personal data in reasoning log inputs; use IQ_CORE_LOG_PATH to direct logs to an appropriate local path and review or remove logs when no longer needed.

Risk: The skill may be invoked broadly for difficult questions and could add unnecessary reasoning overhead to simple tasks.

Mitigation: Use it for complex, uncertain, high-risk, or contradiction-prone tasks, and keep responses concise when the task is simple.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/iq-core)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with optional shell commands and JSONL log records from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional local helper can append reasoning entries to a JSONL file; IQ_CORE_LOG_PATH can override the default path.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
