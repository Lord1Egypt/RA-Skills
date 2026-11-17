## Description:

Long-Term Memory Manager helps agents maintain MEMORY.md and daily memory files by consolidating, archiving, extracting facts, searching history, and generating health summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw long-term memory organized, searchable, and periodically consolidated across MEMORY.md, daily memory files, and archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-term memory files can retain sensitive conversation details or credential-related notes.

Mitigation: Do not store passwords, tokens, recovery codes, OAuth URLs, or sensitive account details in daily memory files; review extracted facts before consolidation or automation.

Risk: Consolidation and archiving can rewrite or move OpenClaw memory files.

Mitigation: Review proposed memory changes and keep recoverable copies before running automated consolidation or archival workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/longterm-memory-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON command output, and generated Markdown memory summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, rewrite, search, and archive files under the OpenClaw memory workspace when its management script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
