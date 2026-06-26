## Description: <br>
Generates Excel insurance rate tables with multi-level headers from product, payment, age, and gender parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyanhe95](https://clawhub.ai/user/liyanhe95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance product and operations teams use this skill to generate standardized Excel rate-table workbooks from product parameters and payment constraints. Agents can run the included local Node.js generator and report the generated workbook location and table structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated rate values are placeholders unless replaced with verified insurance pricing. <br>
Mitigation: Review and replace sample rates with approved pricing data before relying on the workbook for business use. <br>
Risk: The local generator writes a file using the provided product name. <br>
Mitigation: Avoid product names containing path separators or '..' and review the output location before sharing the file. <br>
Risk: The skill runs a local Node.js script with an npm dependency. <br>
Mitigation: Install from the included lockfile in a trusted workspace and review dependency changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyanhe95/insurance-rate-table) <br>
- [保险费率二维表格式标准](references/format-standard.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, shell commands, configuration] <br>
**Output Format:** [Excel workbook plus concise text status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an .xlsx file in the workspace using configurable plans, payment periods, payment methods, receive ages, and age ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
