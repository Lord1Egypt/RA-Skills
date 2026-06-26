## Description: <br>
KingdeeDataExporter guides users through configuring Kingdee K3Cloud credentials and running Python scripts that export configured business documents and reports to multi-sheet Excel files with optional organization and document filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yk-niu](https://clawhub.ai/user/yk-niu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and data teams use this skill to set up and run authorized Kingdee K3Cloud exports for reporting, reconciliation, and spreadsheet analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exports sensitive Kingdee K3Cloud business data. <br>
Mitigation: Use it only with authorization, keep exported Excel files private, and limit scope with --org and --only when possible. <br>
Risk: Kingdee credentials can be exposed if config.py is shared or committed. <br>
Mitigation: Prefer environment variables for credentials and keep local config.py files out of public repositories. <br>
Risk: Optional WeChat webhook delivery can send export information outside the local environment. <br>
Mitigation: Leave WECHAT_WEBHOOK empty or run with --no-wechat unless the destination is approved by the organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yk-niu/kingdee-data-exporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included Python scripts can produce local Excel workbooks when run with authorized Kingdee access.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
