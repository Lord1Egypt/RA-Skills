## Description:

Helps researchers conduct medical systematic reviews and R-based meta-analyses, producing statistical summaries, figures, and reproducible R code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Researchers and clinical evidence teams use this skill to plan systematic reviews, synthesize study results, assess heterogeneity and publication bias, and prepare analysis reports with reproducible code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis summaries are sent to cloud services and could expose sensitive study data.

Mitigation: Review the data and configured services before use; avoid sensitive workspaces until outbound transfers require explicit file selection and per-file confirmation.

Risk: Remote-controlled file transfers may read local files without clear user control.

Mitigation: Require explicit selection and confirmation for each uploaded file before allowing transfers.

Risk: Downloaded files could be written outside the intended output directory.

Mitigation: Constrain download filenames and paths to the designated output directory and confirm each download.

Risk: Custom service endpoints could receive analysis data unexpectedly.

Mitigation: Allowlist approved endpoints and review destination changes before sending data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/medstatstar/skills/meta-analysis)
- [Project homepage (listed in skill metadata; import provenance unavailable)](https://github.com/medstatstar/meta-analysis)
- [User guide](README.md)
- [Systematic review workflow](references/systematic_review_fullflow.md)
- [Analysis reference](references/ADVANCED.md)
- [Workbench](https://meta.app.workbuddy.host/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Analysis reports, tables, figures, and reproducible R code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include forest and funnel plots, statistical summaries, and systematic-review guidance.]

## Skill Version(s):

2.20.1 (source: frontmatter, release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
