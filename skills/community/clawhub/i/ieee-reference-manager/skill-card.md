## Description:

Helps agents review and repair IEEE-style LaTeX and BibTeX references, including citation consistency, required fields, journal macros, DOI metadata, Early Access entries, duplicate detection, and compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlhad](https://clawhub.ai/user/zlhad)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, researchers, and developers working on IEEE-style LaTeX papers use this skill to audit and repair .bib and .tex references, validate DOI metadata, standardize journal names, and generate issue reports or proposed BibTeX edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-provided helper scripts such as analyze_bib.py or nameTranslate.py may execute untrusted code when run by filename.

Mitigation: Use the skill only on trusted LaTeX/BibTeX projects, inspect the exact script contents and path before execution, approve commands explicitly, and run without credentials or unrelated files available.

Risk: DOI and metadata verification can use web access and may return incomplete or mismatched results for new or Early Access papers.

Mitigation: Review DOI lookup results and all proposed reference edits before applying them.

## Reference(s):

- [IEEE Reference Rules](references/ieee-reference-rules.md)
- [Utility Scripts](references/utility-scripts.md)
- [IEEE Reference Guide](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf)
- [IEEEtran BibTeX HOWTO](https://www.michaelshell.org/tex/ieeetran/bibtex/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with BibTeX snippets, inline shell commands, and proposed file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web access for DOI checks and may propose edits to LaTeX or BibTeX files after review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
