## Description: <br>
Mx Macro Data lets agents query Eastmoney macroeconomic data with natural language and save results as CSV files plus a text description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akiry09](https://clawhub.ai/user/akiry09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch specific macroeconomic indicators for market research, policy analysis, and reporting across regions and time periods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user queries to an external Eastmoney service using an API key. <br>
Mitigation: Provide EM_API_KEY only through the environment, confirm the key scope and revocation process, and avoid placing secrets in prompts, logs, or generated files. <br>
Risk: Broad or ambiguous macroeconomic queries can return incomplete, limited, or unintended datasets. <br>
Mitigation: Use specific indicators, commodities, regions, and time scopes, then review the generated CSV and description files before relying on results. <br>
Risk: Set-based requests such as province groups or multiple indicators may require completeness checks across returned files. <br>
Mitigation: Compare expected region and indicator coverage against each frequency-specific CSV and retry targeted missing pairs before final delivery. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akiry09/mx-mx-macro-data) <br>
- [Eastmoney MxClaw service](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Code] <br>
**Output Format:** [CSV files and UTF-8 text description, with CLI or Python API status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and writes one or more frequency-specific CSV files plus a description file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
