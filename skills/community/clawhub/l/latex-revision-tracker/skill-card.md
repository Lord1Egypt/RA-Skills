## Description:

Systematic workflow for tracking, managing, and revising large LaTeX academic papers with version control, content integration, and quality assurance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-of-cosmotim](https://clawhub.ai/user/larry-of-cosmotim)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, graduate students, and collaborative writing teams use this skill to manage revisions for large LaTeX manuscripts, including content integration, bibliography workflows, diff tracking, and pre-submission quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cleanup commands can delete intermediate files if run in the wrong manuscript directory.

Mitigation: Review the working directory and confirm the diff PDF is acceptable before running cleanup commands.

Risk: Git push and tag examples can change a shared remote repository.

Mitigation: Review remote names, branch names, and tag intent before executing version-control commands.

Risk: A single LaTeX compilation pass can leave citations or references unresolved in diff PDFs.

Mitigation: Use the full pdflatex, bibtex, pdflatex, pdflatex workflow for bibliography-bearing manuscript diffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larry-of-cosmotim/skills/latex-revision-tracker)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with checklists and inline bash, LaTeX, and Git examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for user-directed local manuscript and version-control tasks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
