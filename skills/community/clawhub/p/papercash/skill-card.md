## Description:

论文全流程辅助: 8源检索、综述生成、查重预检、降AI率、参考文献格式化、Word导出.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesseovo](https://clawhub.ai/user/jesseovo)

### License/Terms of Use:

MIT-0

## Use Case:

Students and academic writers use PaperCash to search scholarly sources, draft literature reviews and outlines, format citations, run plagiarism prechecks, polish text, and export Word documents. Agents should present results as assistance that requires user review, source verification, and academic-integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research-derived queries and manuscript text may be sent to external academic services during search, plagiarism precheck, citation lookup, or diagnostics.

Mitigation: Avoid confidential, unpublished, or institution-restricted manuscripts unless external service use is acceptable; review generated search terms before use.

Risk: Optional CNKI/Wanfang cookies and Semantic Scholar API keys can be stored in local configuration files.

Mitigation: Store credentials with restrictive file permissions, prefer environment variables when possible, and remove credentials when no longer needed.

Risk: The humanize feature can be misused to conceal AI authorship or violate academic policies.

Mitigation: Use rewriting as editing assistance only, keep the student or author responsible for the final text, and follow institutional disclosure and academic-integrity rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesseovo/skills/papercash)
- [README.md](README.md)
- [User feedback report](docs/user_feedback_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, DOCX files, Shell commands, Configuration guidance]

**Output Format:** [Markdown, compact text, JSON, or exported Word documents depending on the command and flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save outputs to a chosen directory and can export search or review results as .docx files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
