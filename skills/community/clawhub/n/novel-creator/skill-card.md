## Description:

Novel Creator is a Chinese-language fiction workflow for planning, drafting, continuing, restructuring, and style-calibrating long-form novels and serialized web fiction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[km1001](https://clawhub.ai/user/km1001)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users can use this skill to turn Chinese novel ideas, drafts, or stalled projects into structured plans, memory files, style guides, chapter drafts, and continuity updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference guidance embeds an unjustified BL exclusion, which may reduce inclusive or neutral genre support.

Mitigation: Review the reference-material exclusion before installing or using the skill when inclusive genre coverage is required.

Risk: The clean reset path can delete project folders after creating a backup and does not add its own confirmation prompt.

Mitigation: Run initialization only in a dedicated novel project directory, verify the target path, and avoid --clean unless the backup and deletion behavior are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/km1001/skills/novel-creator)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Prompt guide](artifact/references/prompt-guide.md)
- [Chapter guide](artifact/references/chapter-guide.md)
- [Quality checklist](artifact/references/quality-checklist.md)
- [Genre reference index](artifact/references/小说经典片段赏析_总目录.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose and project files with optional shell commands and script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language novel plans, memory records, style guides, chapter drafts, workspace files, and word-count checks.]

## Skill Version(s):

3.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
