## Description:

Intelligently organizes files and folders by analyzing context, finding duplicates, suggesting structures, and automating cleanup with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to analyze messy local folders, find duplicates, propose safer organization plans, and perform approved file moves, renames, archiving, or cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and reorganize broad areas of a local filesystem.

Mitigation: Use explicit target paths, avoid whole-home-directory requests, and review the proposed organization plan before changes are made.

Risk: Moves, renames, archive actions, or duplicate deletion could alter or remove files the user intended to keep.

Mitigation: Require confirmation before destructive actions, log all moves, and review every proposed deletion or duplicate cleanup decision.

Risk: Example shell commands use placeholders that could be unsafe if copied without path validation or quoting.

Mitigation: Quote and validate all paths before running shell commands, especially when paths contain spaces or user-controlled input.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local filesystem operations such as creating folders, moving files, renaming files, and duplicate cleanup after user approval.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
