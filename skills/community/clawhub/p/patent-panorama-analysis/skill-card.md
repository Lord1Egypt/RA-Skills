## Description:

Generates editable HTML patent panorama reports from uploaded patent and technology-breakdown Excel files, covering technology overview, key branches, competitors, patent risk, and patent layout recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and patent analysts use this skill to turn patent spreadsheets and optional technology breakdown spreadsheets into editable HTML reports with statistics, visualizations, competitive analysis, FTO-oriented risk discussion, and layout recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential patent, FTO, or competitor data from uploaded spreadsheets.

Mitigation: Review before installation and confirm before allowing the agent to read sensitive spreadsheets or submit information to external services.

Risk: Generated reports use a mutable third-party ECharts CDN script.

Mitigation: Prefer a version that pins or bundles ECharts locally with integrity verification before using generated reports in sensitive environments.

Risk: Database-backed or real-time conclusions depend on the external PatSnap/Zhihuiya MCP service.

Mitigation: Verify account authorization, MCP configuration, and data-sharing expectations before enabling the service.

## Reference(s):

- [Data Analysis Guide](references/data_analysis_guide.md)
- [Report Structure Guide](references/report_structure.md)
- [UI Style Guide](references/ui_style_guide.md)
- [ECharts 5 CDN](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated editable HTML report code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports use ECharts visualizations and contenteditable text sections; real-time database-backed conclusions require the Zhihuiya MCP service to be configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
