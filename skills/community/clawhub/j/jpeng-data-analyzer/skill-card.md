## Description:

Data analysis and visualization skill. Supports CSV, Excel, JSON data with statistical analysis, charts, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to analyze datasets, generate statistical summaries, clean or transform data, and create visualizations or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running analysis on unintended or sensitive datasets could create derived reports or files that expose data in shared locations.

Mitigation: Run the skill only on datasets the agent is authorized to process and write outputs to an isolated folder.

Risk: Chart, report, or transformed-data outputs could overwrite existing files when directed to shared paths.

Mitigation: Use a dedicated output directory for each run and review generated files before sharing or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-data-analyzer)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON or file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce charts, HTML reports, statistical summaries, and transformed dataset files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
