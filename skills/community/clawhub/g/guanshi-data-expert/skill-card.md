## Description:

观势 — 数据分析专家 helps agents clean structured and semi-structured data, run statistical and financial analysis, create visualizations, and produce decision-ready quantitative insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill when a GuanShi Chief-style workflow needs data cleaning, trend and hypothesis testing, ROI or NPV modeling, sensitivity analysis, chart generation, or scenario simulation from already gathered data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install unpinned Python packages into the active Python environment.

Mitigation: Use a disposable virtual environment, or preinstall reviewed and pinned versions of pandas, numpy, scipy, and matplotlib before enabling the skill.

Risk: Generated labels and reports may assume Chinese-first formatting or localized terminology.

Mitigation: Review outputs when English labels or source-preserved naming are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/guanshi-data-expert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, statistical notes, code snippets, shell commands, and chart file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG chart files in an output directory and intermediate working files in a temp directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
