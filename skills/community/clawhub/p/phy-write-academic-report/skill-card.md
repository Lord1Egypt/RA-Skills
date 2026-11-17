## Description:

Write 40-100+ page academic reports, theses, dissertations, and technical reports with a 3-wave workflow that extracts research data, drafts chapters in parallel, and compiles LaTeX with citation and cross-reference checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External students, researchers, and developers use this skill to turn a research repository with code, results, figures, and bibliography needs into a long-form LaTeX thesis, dissertation, final year project report, or technical report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt broad repository reading and file writing while orchestrating background agents.

Mitigation: Run it only on a copy of the research repository or a dedicated output directory and require confirmation before launching background agents.

Risk: The workflow may compile LaTeX and run local scripts that inspect or modify report files.

Mitigation: Review the workflow before execution, pin dependencies in a virtual environment, and inspect generated files before use.

Risk: Citation checks may send bibliography titles, authors, DOIs, or unpublished project details to external APIs.

Mitigation: Disable or avoid citation API checks for confidential or unpublished bibliography data.

Risk: The security evidence reports an unsafe remote installer recommendation.

Mitigation: Avoid curl-to-shell installation and install dependencies through reviewed package-manager commands or a pinned virtual environment.

## Reference(s):

- [Citation Verification Workflow](artifact/references/citation-workflow.md)
- [Compilation Guide](artifact/references/compilation-guide.md)
- [Parallel Pipeline](artifact/references/parallel-pipeline.md)
- [Writing Guide](artifact/references/writing-guide.md)
- [Cross-Reference Audit Script](artifact/scripts/cross_ref_audit.py)
- [Citation Checker Script](artifact/scripts/citation_checker.py)
- [ml-paper-writing](https://github.com/Orchestra-Research/ml-paper-writing)
- [Canlah AI Homepage](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-write-academic-report)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with LaTeX, BibTeX, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report plans, chapter drafts, LaTeX project files, citation checks, cross-reference audit commands, and compilation guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
