## Description: <br>
Inventory Anomaly helps agents generate a local inventory anomaly detection and demand forecasting system with Excel data handling, ARIMA-based forecasting, restock recommendations, and TXT reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawvincent](https://clawhub.ai/user/openclawvincent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams can use this skill to scaffold a spare-parts inventory analytics project that reads Excel workbooks, detects stock and demand anomalies, forecasts short-term demand, and produces replenishment reports. It is aimed at manufacturing, retail, and spare-parts management workflows that need customizable local templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project templates can write data/spare_parts.xlsx and output/report.txt in the target project. <br>
Mitigation: Run in a dedicated project directory and back up any real inventory workbook before generating or updating data. <br>
Risk: The generated project depends on pandas, numpy, statsmodels, and openpyxl. <br>
Mitigation: Install dependencies in a virtual environment and pin reviewed versions for production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawvincent/inventory-anomaly) <br>
- [Publisher profile](https://clawhub.ai/user/openclawvincent) <br>
- [README.md](README.md) <br>
- [requirements.txt](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project templates that read and write Excel workbooks and generate TXT reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
