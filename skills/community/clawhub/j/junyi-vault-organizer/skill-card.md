## Description:

Junyi Vault Organizer helps an agent classify and save text notes into a two-domain Obsidian knowledge vault for business and life-learning content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanranc](https://clawhub.ai/user/xuanranc)

### License/Terms of Use:

MIT-0

## Use Case:

External users who maintain an Obsidian vault use this skill to route, structure, and persist text notes across business and life-learning domains. It supports capture, distillation, naming, traceability, and optional file writing for organized markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local files into an Obsidian vault, so an incorrect or ambiguous target path could place content in the wrong location.

Mitigation: Require an explicit vault_path and business_name before use, preview the exact target path and content, and ask for confirmation when the save location is ambiguous.

Risk: The bundled writer has under-scoped filesystem write behavior when invoked directly.

Mitigation: Avoid invoking chunk_writer.py directly unless it is fixed to require a vault root, reject extensionless and out-of-vault paths, and use atomic writes to reduce accidental data loss.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanranc/skills/junyi-vault-organizer)
- [Publisher profile](https://clawhub.ai/user/xuanranc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, routing guidance, configuration guidance, and shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only Obsidian vault content; long content may be written in chunks up to 20000 characters each.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
