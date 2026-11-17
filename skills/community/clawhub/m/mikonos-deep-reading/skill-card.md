## Description:

Turns books, long articles, research reports, and papers into a connected Zettelkasten knowledge network with structure notes, atomic notes, method notes, and index notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikonos](https://clawhub.ai/user/mikonos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to deeply digest books, long-form articles, research reports, or papers into an organized knowledge vault. It guides agents through planning, structure extraction, concept note creation, methodology capture, index onboarding, network review, and workflow audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify and reorganize an existing knowledge vault, including index files and note locations.

Mitigation: Use the skill in a bounded vault or review proposed file edits and moves before allowing changes to existing indexes or note directories.

Risk: The workflow can call companion skills and require remediation writes during the audit phase.

Mitigation: Review companion skill calls and workflow-audit remediation before execution, especially when they affect existing notes or indexes.

Risk: Generated reading notes may preserve unverified claims when the source material is unavailable or only summarized.

Mitigation: Require source-status labels in notes and review case-fidelity sections before relying on extracted claims.

## Reference(s):

- [Expert Personas](references/expert_personas.md)
- [Luhmann Scan Workflow](references/luhmann_scan.md)
- [Atomic Note Template](templates/atomic_note_template.md)
- [Index Note Template](templates/index_note_template.md)
- [Method Note Template](templates/method_note_template.md)
- [Structure Note Template](templates/structure_note_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown notes with YAML frontmatter, wikilinks, checklists, tables, and task-tracking sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and reorganizes vault notes, including structure notes, atomic notes, method notes, index notes, execution plans, task tracking, and audit reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
