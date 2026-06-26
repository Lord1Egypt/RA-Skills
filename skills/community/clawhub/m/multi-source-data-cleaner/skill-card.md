## Description: <br>
Cleans, deduplicates, normalizes, classifies, merges, and exports multi-format tabular datasets, with optional AI-assisted field identification and Feishu outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, CRM, ecommerce, finance, and support teams use this skill to turn messy Excel, CSV, TSV, JSON, or pasted tabular data into cleaned files, joined datasets, tags, and quality reports. Developers and agents can call the Python or CLI entry points to automate data-cleaning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive datasets or samples can be sent to external AI providers when ai_model or AI classification is enabled. <br>
Mitigation: Use local-only operation for sensitive data by leaving ai_model unset, setting classify to false unless needed, and avoiding DATA_CLEANER_API_KEY for AI features. <br>
Risk: Cleaned records and quality reports can be uploaded to Feishu when Bitable or document output is enabled. <br>
Mitigation: Enable bitable_output, Feishu document creation, folder tokens, and report generation only when the destination workspace is approved for the dataset. <br>
Risk: DATA_CLEANER_API_KEY and Feishu tokens are sensitive credentials. <br>
Mitigation: Store credentials in managed environment variables, restrict access to the runtime, and rotate keys if logs, reports, or shared workspaces may expose them. <br>
Risk: The README claims local-only processing, but release security evidence says external data flows are understated. <br>
Mitigation: Review the configured features before deployment and document which external services are allowed for each workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiji0802/multi-source-data-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/qiji0802) <br>
- [MiniMax platform](https://platform.minimax.chat/) <br>
- [DeepSeek platform](https://platform.deepseek.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Excel, CSV, Markdown reports, Python dictionaries, CLI output, and optional Feishu Bitable or document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process sensitive tabular data locally or send samples, cleaned records, reports, tokens, or API keys to configured external AI, license-validation, and Feishu services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact documentation lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
