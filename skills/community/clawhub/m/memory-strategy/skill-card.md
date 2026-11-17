## Description:

Memory Strategy helps agents manage conversational memory with long-term and short-term stores, 30-day time decay, 1-5 importance scoring, trigger-based writes, retrieval rules, and silent session cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugoiku](https://clawhub.ai/user/hugoiku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide what conversation details to save, retrieve, decay, archive, or discard across sessions. It is most useful for workflows that need persistent preferences, project notes, decisions, patterns, and recent activity logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation content into long-term and short-term memory, including session-end cleanup behavior.

Mitigation: Review what data may be stored, require explicit approval before long-term writes, and disable silent auto-write unless the workflow is trusted.

Risk: The memory layout can store sensitive personal data or secrets in plain text files.

Mitigation: Do not store API keys, tokens, passwords, private keys, or sensitive personal data in memory files.

Risk: Automatic importance scoring may send text to an external Kimi API.

Mitigation: Avoid external scoring for confidential text unless privacy terms, consent, redaction, and retention controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugoiku/skills/memory-strategy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce memory directory layouts, scoring guidance, retrieval instructions, cleanup reports, and script invocation examples.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
