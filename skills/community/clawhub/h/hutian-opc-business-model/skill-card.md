## Description: <br>
Analyzes business plans to produce PESTL analysis, Boston Matrix positioning, SWOT analysis, a business model canvas, dimensional scores, and radar-chart reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and business consultants use this skill to turn business-plan documents into structured commercial-model analysis, scoring, strategy recommendations, and visual reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may load remote ECharts JavaScript that can access report contents, which is sensitive for confidential business plans. <br>
Mitigation: Use PNG output for confidential material, or bundle ECharts locally and escape report fields before opening generated HTML. <br>
Risk: Business-model recommendations can be misleading if source documents omit key facts or if inferred items are treated as verified. <br>
Mitigation: Review missing-information prompts, keep unsupported findings marked as missing or inferred, and validate strategic conclusions before business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/hutian-opc-business-model) <br>
- [Publisher profile](https://clawhub.ai/user/golngod) <br>
- [README.md](README.md) <br>
- [PESTL analysis template](references/01-PESTL分析模板.md) <br>
- [Boston Matrix template](references/02-波士顿矩阵模板.md) <br>
- [SWOT analysis template](references/03-SWOT分析模板.md) <br>
- [Business model canvas template](references/04-画布九宫格模板.md) <br>
- [Radar chart generation guide](references/07-雷达图生成说明.md) <br>
- [Comprehensive diagnosis framework](references/08-综合诊断框架.md) <br>
- [Report output template](references/10-报告输出模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional HTML radar-chart output and chart configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts PDF, Word, or text business-plan inputs; asks follow-up questions when key facts are missing and marks unsupported findings rather than inventing them.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
