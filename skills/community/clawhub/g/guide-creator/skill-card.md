## Description:

Creates and maintains a standardized Chinese-language project guide system, including start.md and guide/ documents for design, architecture, plans, changelogs, pitfalls, and context recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revolgmphl](https://clawhub.ai/user/revolgmphl)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to initialize and maintain structured project documentation for ongoing development work. It helps create project overviews, technical architecture notes, development plans, changelogs, pitfalls records, and context-recovery material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation may be written to the wrong project root or existing guide files may be overwritten.

Mitigation: Review the target --root before running scripts and avoid --force unless overwriting documentation is intended.

Risk: Future agents may read guide notes and pitfalls as project context.

Mitigation: Review generated documentation for accuracy, sensitive content, and misleading instructions before relying on it as context.

Risk: Project documentation can become stale or inconsistent after code changes.

Mitigation: Synchronize changelog entries, guide version metadata, and file inventories after feature work, bug fixes, new files, and architecture changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/revolgmphl/skills/guide-creator)
- [Guide System Specification](references/guide-spec.md)
- [Start Document Template](references/templates/start-template.md)
- [Guide Overview Template](references/templates/guide-template.md)
- [Changelog Template](references/templates/changelog-template.md)
- [Pitfalls Template](references/templates/pitfalls-template.md)
- [Sub-document Templates](references/templates/sub-doc-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, concise guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update start.md and guide/ documentation under the selected project root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
