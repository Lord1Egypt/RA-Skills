## Description: <br>
Audit OpenClaw configuration for security risks and generate a remediation report using the user's configured LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Muhammad-Waleed381](https://clawhub.ai/user/Muhammad-Waleed381) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local OpenClaw configuration for security gaps and generate a prioritized remediation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw configuration and analyzes redacted findings through the user's configured LLM. <br>
Mitigation: Install only if that local data flow is acceptable; use a local model for sensitive deployments and verify reports do not include token or API key values. <br>
Risk: Generated security findings and remediation guidance may need review for a specific OpenClaw deployment. <br>
Mitigation: Review the report before applying changes and re-run the audit after remediation to confirm the configuration state. <br>
Risk: The skill depends on local command-line tools to read and parse the selected configuration file. <br>
Mitigation: Run it only against intended OpenClaw config paths and confirm the required local tools are available before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Muhammad-Waleed381/openclaw-security-auditor) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Security Checks](artifact/docs/SECURITY-CHECKS.md) <br>
- [Installation Guide](artifact/docs/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security audit report with a risk score, severity-grouped findings, example configuration fixes, and a remediation roadmap.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should describe configuration metadata only and avoid emitting actual secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
