## Description:

Analyzes user-provided academic papers from PDFs or URLs and generates a detailed two-mode reading report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to extract full text from academic papers, identify research questions, methods, findings, and contributions, and produce a Markdown reading report for expert and general audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's activation scope is broader than academic paper analysis.

Mitigation: Tighten invocation criteria so it activates only for user-provided paper, PDF, DOI, or arXiv-style analysis tasks.

Risk: The skill may download documents, execute commands, and create local files.

Mitigation: Limit downloads and file writes to explicit user-provided paper-processing workflows and review commands before execution.

Risk: Temporary analysis files and extracted paper text may contain sensitive or unpublished research content.

Mitigation: Keep generated files scoped to the active task, avoid unnecessary retention, and follow the user's data-handling requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with intermediate text analysis and optional JSON-style execution summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary analysis files and a final paper reading report.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
