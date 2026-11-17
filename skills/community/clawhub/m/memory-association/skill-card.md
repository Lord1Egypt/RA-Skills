## Description:

Memory Association helps an agent recall indexed prior task context before new work, analysis, problem solving, or questions about past work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxiao-code](https://clawhub.ai/user/wuxiao-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to recall relevant project memory before starting tasks, analyzing requirements, solving problems, or answering questions about prior work. It is intended to reduce repeated work and preserve context continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad memory recall can surface sensitive project history, credentials, client details, or externally supplied notes.

Mitigation: Review memory contents before installation and use the skill only in workspaces where broad recall is acceptable.

Risk: Persistent memory and index updates can carry untrusted memory text into future agent context.

Mitigation: Review proposed memory, index, and .learnings updates before accepting them, and avoid storing secrets or untrusted instructions as reusable memory.

Risk: The index builder updates persistent OpenClaw memory files when run outside dry-run mode.

Mitigation: Require explicit approval before running scripts/build_index.py or any workflow that writes daily memory, project memory, or learning files.

## Reference(s):

- [Memory Index](references/MEMORY_INDEX.md)
- [Task Association Examples](references/TASK_ASSOCIATION_EXAMPLES.md)
- [ClawHub Skill Page](https://clawhub.ai/wuxiao-code/skills/memory-association)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write persistent memory and index updates when invoked by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
