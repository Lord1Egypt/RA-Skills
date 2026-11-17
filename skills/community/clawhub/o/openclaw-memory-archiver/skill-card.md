## Description:

Archives older memory logs into compressed files, extracts key decisions, context, and tasks into long-term memory, and cleans up expired source logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to periodically archive stale memory/*.md logs, preserve important decisions, context, and tasks in MEMORY.md, and reduce storage by compressing old logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archived originals can be deleted by default after summarization, which may remove verbatim memory logs users later need.

Mitigation: Confirm archive settings before running, keep backups, or set delete_after_archive to false when verbatim logs must be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangkai258/skills/openclaw-memory-archiver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, create zip archives under memory/archive/, and delete archived source logs when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
