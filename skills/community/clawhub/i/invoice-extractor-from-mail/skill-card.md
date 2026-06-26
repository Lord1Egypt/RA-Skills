## Description: <br>
Designed for AP finance teams in cross-border trade enterprises, this skill helps fetch invoice attachments from email or local files, extract key invoice fields with ADP, and export results to Excel files or business systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeane-li](https://clawhub.ai/user/jeane-li) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Finance and audit teams use this skill to collect invoice attachments from mailboxes or local folders, run ADP invoice extraction, map extracted fields, and prepare results for Excel, cloud upload, or business-system ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive mailbox, ADP, cloud, and ERP credentials. <br>
Mitigation: Use a dedicated test mailbox or narrow folder, apply least-privilege OAuth/API scopes, store secrets in a proper secret manager, and keep a revocation plan. <br>
Risk: The skill includes remote installer commands for the ADP CLI. <br>
Mitigation: Do not run remote installer commands blindly; install only from a trusted, reviewed, and pinned source. <br>
Risk: Pushing extracted invoice data directly into business systems can propagate mapping or extraction errors. <br>
Mitigation: Export to local Excel first and verify extraction results and field mappings before enabling business-system API push. <br>


## Reference(s): <br>
- [ADP Invoice/Receipt Extraction Field Schema Reference](refers/adp-invoice-fields.md) <br>
- [ADP Portal - Chinese Mainland](https://adp.laiye.com/) <br>
- [ADP Portal - Outside Chinese Mainland](https://adp-global.laiye.com/) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local Excel files, failed-record logs, and business-system API request payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
