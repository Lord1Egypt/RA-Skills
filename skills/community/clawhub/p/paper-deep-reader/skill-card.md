## Description:

Paper Deep Reader helps agents deeply analyze one selected research paper and produce an evidence-based markdown note, technical summary, critique, or implementation memo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soymilkwinsagain](https://clawhub.ai/user/soymilkwinsagain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical readers use this skill to guide an agent through deep analysis of a single selected paper and produce reusable notes that reconstruct the paper's technical mechanism, evidence, assumptions, and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Script-generated paper maps, notation tables, claim matrices, and limitation ledgers are heuristic drafts and can misstate a paper if not checked.

Mitigation: Review generated artifacts against the source paper before using them in a final note.

Risk: The release security guidance reports a missing shared script module and inconsistent reference paths, which may make the scripted workflow unreliable.

Mitigation: Confirm helper modules and reference paths before relying on local scripts; fall back to the manual reading workflow if scripts fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soymilkwinsagain/skills/paper-deep-reader)
- [Reading workflow](references/reading-workflow.md)
- [Routing rules](references/routing-rules.md)
- [Output contract](references/output-contract.md)
- [Paper taxonomy](references/paper-taxonomy.md)
- [Base note template](references/note-template-base.md)
- [Script workflow](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reading notes with YAML frontmatter, markdown tables, and optional script-generated draft artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for one selected paper at a time; script-generated tables are heuristic drafts that require review.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
