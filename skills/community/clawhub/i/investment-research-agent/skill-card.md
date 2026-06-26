## Description: <br>
麦赛尔夫 is a US stock investment research agent that searches public financial data, performs fundamental analysis, and writes concise sourced Markdown reports without subjective investment recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzed2](https://clawhub.ai/user/yuzed2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment research teams use this skill to configure an OpenClaw agent for public-source US equity research, financial data collection, valuation tables, and sourced report writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial research outputs may be mistaken for investment advice or relied on without checking source freshness. <br>
Mitigation: Treat reports as research references, review the cited sources and dates, and apply the skill's recency rules for prices, latest financial periods, and forward forecasts. <br>
Risk: The skill writes research files and memory logs in the local workspace. <br>
Mitigation: Run it in a scoped workspace and review generated files before sharing or using them in downstream workflows. <br>
Risk: Large document parsing may require optional package installation. <br>
Mitigation: Approve any package installation manually and prefer an isolated virtual environment for document-processing dependencies. <br>


## Reference(s): <br>
- [Research Methodology](references/methodology.md) <br>
- [Report Structure Reference](references/report-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with inline source links, configuration templates, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports require inline citations, current financial periods, three forward forecast years, English file paths, and workspace memory log updates.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
