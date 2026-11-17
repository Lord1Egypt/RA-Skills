## Description:

Adds relevant academic citations to research paper projects by inspecting TeX and BibTeX files, inserting citation markers, and producing an ADD.MD report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldglycine](https://clawhub.ai/user/oldglycine)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and writing agents use this skill to add non-duplicate citation markers to Overleaf-style paper projects and document the inserted references in an ADD.MD report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite paper files and may not create the promised backup.

Mitigation: Run it only on a copied project or a version-controlled working tree, and verify backups before accepting changes.

Risk: An unchecked report path can overwrite files outside the intended paper project.

Mitigation: Keep the report path relative to the paper project and review the resolved output path before execution.

Risk: Unpinned dependencies and the documented pdflatex pip package may introduce supply-chain or runtime risk.

Mitigation: Use an isolated environment with version-pinned dependencies and independently verify any LaTeX tooling.

## Reference(s):

- [Code Reference](reference/CODE.MD)
- [Backup Reference](reference/BACKUP.MD)
- [Citation Reference](reference/REFERENCES.MD)
- [ClawHub Skill Page](https://clawhub.ai/oldglycine/skills/oldglycine-paper-reference-adder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell commands; the runner writes TeX edits and an ADD.MD report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify TeX files in the target project and write a report file.]

## Skill Version(s):

1.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
