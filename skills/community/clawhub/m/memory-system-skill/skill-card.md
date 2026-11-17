## Description:

A practical memory protocol for long-running AI agents: dual logs, encoding safety, backup sync, multi-agent facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heicha1231414](https://clawhub.ai/user/heicha1231414)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give long-running AI agents a practical protocol for persistent memory, daily logging, backup verification, and session startup continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent verbatim conversation memory can retain sensitive, secret, or personal data longer than intended.

Mitigation: Use the skill only where users have consented to persistent memory, and add secret and PII redaction, restrictive permissions, encryption, retention limits, and deletion procedures before deployment.

Risk: Stored transcripts and mirrored memory files can be misused as future instructions if an agent treats them as executable guidance.

Mitigation: Require agents to treat stored transcripts as quoted data, not instructions, and review retrieved memory before using it to affect behavior.

Risk: Broad log mirroring and stale backup locations can increase privacy exposure and make old copies difficult to govern.

Mitigation: Limit mirror locations, document authoritative copies and deprecated paths, verify checksums after sync, and apply the same access controls and deletion process to every mirror.

## Reference(s):

- [Memory System Protocol README](README.md)
- [Memory System Protocol v3](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with filesystem layout examples, checklists, and shell-oriented operating procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces operational guidance for agents; it does not provide executable code or call external services.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
