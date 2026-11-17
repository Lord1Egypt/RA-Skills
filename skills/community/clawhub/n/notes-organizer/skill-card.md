## Description:

A note organization and knowledge-linking tool that analyzes the directory structure, reorganizes notes according to the user's chosen classification scheme, and adds Obsidian-style bidirectional links between highly related topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youningnihaobang](https://clawhub.ai/user/youningnihaobang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and knowledge workers use this skill to reorganize Markdown or Obsidian note collections, choose a classification scheme, and optionally add bidirectional links between related notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The organizer can mass-move Markdown files and rewrite note contents without a preview.

Mitigation: Run it only on a backed-up notes folder and review the selected classification and linking options before execution.

Risk: Custom category or subdirectory names may affect where files are created or moved.

Mitigation: Avoid names containing slashes, absolute paths, or `..`.

Risk: The documentation advertises undo or backup support, but the security guidance says not to rely on it.

Mitigation: Maintain an external backup or version-controlled copy before using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youningnihaobang/skills/notes-organizer)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, command-line prompts, Obsidian-style links, and local note file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May move Markdown files, edit note contents, and write .organize_log.json in the selected notes directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
