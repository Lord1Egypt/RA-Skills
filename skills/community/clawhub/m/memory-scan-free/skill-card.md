## Description: <br>
Memory Scan helps audit AI agent memory and workspace configuration files for malicious instructions, prompt injection, credential leakage, and related risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan agent memory files and workspace configuration documents, review categorized security findings, and optionally quarantine confirmed risky lines after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive memory or configuration data could be exposed if optional callback_url or API-key behavior causes outbound communication that is not clearly documented. <br>
Mitigation: Use only when an explicit memory/configuration scan is intended; avoid callback_url and API keys in sensitive workspaces unless the publisher clarifies network behavior. <br>
Risk: Quarantine actions can modify memory files by replacing selected lines. <br>
Mitigation: Confirm the target file and line before quarantine, and use the documented backup and restore flow if a line is quarantined incorrectly. <br>
Risk: Pattern-based scanning may miss semantic prompt injection, indirect instructions, or credentials that do not match known prefixes. <br>
Mitigation: Treat low-severity or clean results as limited scan findings, and manually review high-value memory files or use a trusted deeper scanner for sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-scan-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown scan guidance and reports, with optional JSON output for findings and execution logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings can include file paths, line numbers, severity levels, threat categories, suggested actions, and user-confirmed quarantine or restore commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
