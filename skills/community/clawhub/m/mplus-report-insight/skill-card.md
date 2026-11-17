## Description:

自动解析 Mplus 输出文件，提取拟合指数和标准化参数，生成 APA 风格图表与可引用的 PDF 分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lz0311-zhen](https://clawhub.ai/user/lz0311-zhen)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts in psychology, management, education, and related social science fields use this skill to summarize Mplus CFA/SEM output, compare model fit, visualize standardized parameters, and draft APA-style analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published artifact documents scripts and reference files that are not included in the release.

Mitigation: Review any separately obtained scripts or dependencies before execution, and verify that they match the documented report-generation workflow.

Risk: Automated fit-threshold and significance interpretations can be incomplete for a specific research design, sample, or correction strategy.

Mitigation: Treat generated interpretations as draft analysis support and have the responsible researcher verify thresholds, p-value handling, and final conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lz0311-zhen/skills/mplus-report-insight)
- [Published skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated report files such as PDF charts and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid Mplus .out file with model fit information and STDYX standardization sections; final statistical conclusions should be reviewed by the researcher.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
