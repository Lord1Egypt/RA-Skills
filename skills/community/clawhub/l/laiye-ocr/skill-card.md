## Description: <br>
Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity and credential documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External users, business operators, and agent developers use this skill to parse documents, extract structured fields, query processing tasks, and manage custom extraction applications through the Laiye ADP CLI. It is suited to finance, administrative, HR, procurement, and document automation workflows that need JSON-ready OCR and extraction results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends document contents to Laiye-hosted cloud services, which may expose sensitive IDs, HR files, invoices, contracts, or other regulated information. <br>
Mitigation: Use it only after confirming approval to process those documents with Laiye ADP and understanding the service's data handling terms. <br>
Risk: The skill requires API credentials and can write batch outputs containing sensitive extracted data. <br>
Mitigation: Store API keys securely, avoid sharing credentials in prompts or logs, and write exported results only to restricted directories. <br>
Risk: The artifact documents remote installer commands that pipe downloaded scripts into a shell. <br>
Mitigation: Prefer a pinned package installation, or inspect and verify downloaded installer scripts before execution. <br>
Risk: The service uses credits and may incur commercial cost for document parsing, invoice extraction, order extraction, or custom extraction. <br>
Mitigation: Check the account credit balance and confirm the intended processing scope before running batch or high-volume jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/laiye-ocr) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [Command Reference](references/commands.md) <br>
- [Response Schema Reference](references/response-schema.md) <br>
- [Error Handling Guide](references/error-handling.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI returns structured JSON for parsing, extraction, task query, configuration, app management, and credit-balance operations.] <br>

## Skill Version(s): <br>
1.10.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
