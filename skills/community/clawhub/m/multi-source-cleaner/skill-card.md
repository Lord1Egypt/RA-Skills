## Description: <br>
Multi-Source Cleaner parses messy Excel, CSV, TSV, JSON, and pasted text sources, identifies fields, cleans and merges records, and exports cleaned datasets and quality reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yk-global-01](https://clawhub.ai/user/yk-global-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operational teams use this skill to standardize, deduplicate, complete, classify, and merge tabular business data from multiple sources before exporting usable datasets and quality reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill under-discloses external transfers of dataset samples, reports, and credential-like values while claiming data stays local. <br>
Mitigation: Use local-only cleaning unless external AI and Feishu exports are explicitly needed, and review disclosure, consent, redaction, and endpoint controls before processing sensitive data. <br>
Risk: DATA_CLEANER_API_KEY is used both for AI provider calls and subscription token verification behavior in the artifact. <br>
Mitigation: Avoid placing third-party AI secrets in DATA_CLEANER_API_KEY until license and AI credentials are separated or otherwise clearly documented and controlled. <br>
Risk: AI-assisted field identification and classification can send column samples or row samples to configured MiniMax or DeepSeek endpoints. <br>
Mitigation: Disable AI features or redact samples when processing personal, regulated, confidential, or customer data. <br>
Risk: Feishu export paths can create Bitable records and cloud documents from cleaned data and reports. <br>
Mitigation: Enable Feishu output only with approved workspace credentials, destination folders, and sharing controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yk-global-01/multi-source-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/yk-global-01) <br>
- [MiniMax platform](https://platform.minimax.chat/) <br>
- [DeepSeek platform](https://platform.deepseek.com/) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, markdown, text] <br>
**Output Format:** [Python pipeline results, CLI output, CSV/XLSX files, Markdown quality reports, and optional Feishu Bitable or document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can require DATA_CLEANER_API_KEY, DATA_CLEANER_TIER, and optional Feishu folder or user identifiers for AI, subscription, and Feishu export flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
