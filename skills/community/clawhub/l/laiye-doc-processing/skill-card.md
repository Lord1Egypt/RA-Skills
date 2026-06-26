## Description: <br>
Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity & credential documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeane-li](https://clawhub.ai/user/jeane-li) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Developers, AI agent builders, and business operations teams use this skill to install and operate Laiye ADP CLI workflows for document parsing, structured field extraction, application selection, batch jobs, and result querying. It supports finance, administration, HR data entry, and system integration workflows that need JSON document-processing output. <br>

### Deployment Geography for Use: <br>
Global, with separate Chinese Mainland and overseas Laiye ADP service endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on the external Laiye ADP CLI and service. <br>
Mitigation: Install only from trusted Laiye ADP sources, prefer the documented npm install path, and avoid curl-to-bash or downloaded PowerShell scripts unless the source and contents are reviewed. <br>
Risk: Documents selected for parsing or extraction can be sent to Laiye ADP. <br>
Mitigation: Avoid uploading regulated or confidential documents without approval, confirm exact files and folders before batch jobs, and store exported results in a protected location. <br>
Risk: The skill requires ADP credentials and can consume paid service credits. <br>
Mitigation: Use a dedicated ADP API key, protect credentials, check credit balance and billing rules before large jobs, and confirm costs before batch processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeane-li/laiye-doc-processing) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [Command reference](references/commands.md) <br>
- [Response schema](references/response-schema.md) <br>
- [Error handling guide](references/error-handling.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run Laiye ADP CLI commands that return document parsing and extraction results as JSON.] <br>

## Skill Version(s): <br>
1.10.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
