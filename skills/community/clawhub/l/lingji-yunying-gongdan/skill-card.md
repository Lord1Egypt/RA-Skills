## Description:

对中国移动"灵畿"平台工单数据进行全面分析，支持时效、满意度、热点问题评估并生成专业PDF运营报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyusheng188](https://clawhub.ai/user/chengyusheng188)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and support teams use this skill to analyze LingJi platform ticket Excel exports, monitor response timeliness, satisfaction, workload, and hotspot issues, and generate reports for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket exports and generated reports may contain sensitive internal data.

Mitigation: Use only authorized exports in a dedicated, least-privileged environment and treat terminal output, PDFs, and temporary HTML as sensitive internal data.

Risk: The PDF workflow renders workbook-derived values through browser-based HTML generation.

Mitigation: Avoid untrusted workbooks until workbook values are HTML-escaped and browser JavaScript and network access are constrained.

Risk: External report sharing can expose ticket details outside approved channels.

Mitigation: Share generated reports only through organization-approved systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyusheng188/skills/lingji-yunying-gongdan)
- [Publisher profile](https://clawhub.ai/user/chengyusheng188)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Terminal text reports and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Excel workbooks, prints analysis summaries in terminal mode, and writes PDF reports to the requested output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
