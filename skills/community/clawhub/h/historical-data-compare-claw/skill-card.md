## Description: <br>
Historical Data Compare Claw helps agents compare Excel, CSV, or exported historical datasets to calculate period-over-period, year-over-year, trend, and variance analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operators, and agent users use this skill to compare historical metrics across periods, identify meaningful changes, and prepare concise variance and trend reports. It is useful for monthly, quarterly, daily, and year-over-year comparisons across dimensions such as region, category, or channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local datasets that may contain sensitive or unintended data. <br>
Mitigation: Use only data files intended for analysis and confirm selected date and metric columns before running comparisons. <br>
Risk: The optional output path can create or overwrite a report file. <br>
Mitigation: Choose the output path deliberately and review it before execution. <br>
Risk: Excel or data-processing dependencies may need to be installed in the runtime environment. <br>
Mitigation: Install pandas and any Excel-reading dependencies only from trusted package sources. <br>


## Reference(s): <br>
- [Historical Data Compare Claw on ClawHub](https://clawhub.ai/tujinsama/historical-data-compare-claw) <br>
- [Data Analysis Methodology Reference](references/methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown reports, plain-text comparison tables, and optional report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read local CSV or Excel files and optionally write a comparison report to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
