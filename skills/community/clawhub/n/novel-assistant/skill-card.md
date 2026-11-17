## Description:

Novel Assistant helps agents create and continue long-form fiction while maintaining character, worldbuilding, plot, foreshadowing, timeline, memory compression, backups, multi-project organization, and dialogue-style consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnskycn](https://clawhub.ai/user/cnskycn)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and collaborating authors use this skill to draft and continue serialized or long-form novels while keeping memory files, character voices, timelines, foreshadowing, chapter backups, and multiple projects organized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell memory-compression script may execute unintended commands through an unsafe --keep-chapters value.

Mitigation: Use the Python compressor or fix the shell script to accept only plain positive integers before deployment.

Risk: Git-based collaboration can move unpublished drafts or memory files outside the local machine.

Mitigation: Keep novel memory files in a dedicated workspace, review tracked files before pushing, and use a private remote for any synchronization.

Risk: The skill can update or compress memory files and chapter backups that writers rely on for continuity.

Mitigation: Review proposed file changes before applying them and keep recoverable backups or version history for active projects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cnskycn/skills/novel-assistant)
- [Publisher Profile](https://clawhub.ai/user/cnskycn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, structured reports, memory-file templates, shell commands, and local file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide updates to novel memory files, chapter backups, Git-managed drafts, and optional memory compression scripts.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
