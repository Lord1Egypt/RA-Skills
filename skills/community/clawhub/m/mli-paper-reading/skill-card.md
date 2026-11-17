## Description:

Mli Paper Reading helps agents triage, deeply read, critique, compare, and plan reproduction for academic papers from arXiv links, PDFs, DOIs, titles, or paper lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengheliu](https://clawhub.ai/user/pengheliu)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to turn academic papers into structured reading notes, evidence led critiques, comparison tables, literature maps, and reproduction plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML notes may include paper-derived text from untrusted PDFs and render it in a browser.

Mitigation: Escape or sanitize paper-derived text before writing HTML, and use caution with PDFs from untrusted sources.

Risk: The skill can write notes under ~/paper-notes, launch a local web server, and open a browser.

Mitigation: Install and run it only when those local file and browser actions are acceptable for the environment.

Risk: Dependency installation for PDF image extraction can pull a package at install time.

Mitigation: Pin and review dependencies such as pymupdf before installing them.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/PengheLiu/mli-paper-reading-skill/tree/main/skills/mli-paper-reading)
- [ClawHub skill page](https://clawhub.ai/pengheliu/skills/mli-paper-reading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code blocks and generated local HTML reading notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write notes under ~/paper-notes, start a local web server, and open a browser for the generated paper notes.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
