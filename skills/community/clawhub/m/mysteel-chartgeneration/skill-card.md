## Description: <br>
Generates ECharts visualizations from text descriptions or structured data for trend, comparison, and structural charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn chart requests, embedded data, or structured datasets into ECharts configuration and interactive HTML chart files for reports and analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be persisted in project files. <br>
Mitigation: Use a secret store or environment variable, avoid committing key files, and rotate any key that may have been exposed. <br>
Risk: Chart prompts and data are sent to an external provider. <br>
Mitigation: Use only approved datasets, minimize submitted data, and avoid sensitive, regulated, or proprietary information unless the provider is authorized. <br>
Risk: Strict mode may rely on automatically generated Python execution. <br>
Mitigation: Review generated code before execution and run it only in an approved sandbox, or disable that path when review is not possible. <br>


## Reference(s): <br>
- [API Parameters](references/api-parameters.md) <br>
- [Mysteel AI chart generation API](https://mcp.mysteel.com/mcp/info/genie-tool/v1/tool/ai-chart) <br>
- [ClawHub skill page](https://clawhub.ai/wyb92/mysteel-chartgeneration) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [JSON chart configuration and rendered HTML files, with Markdown-style command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Synchronous generation only; outputs include ECharts option JSON, metadata JSON, and interactive HTML files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
