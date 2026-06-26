## Description: <br>
Automatically detects and blocks prompt injection attempts during AI content submission to social media, APIs, web forms, and file outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danlct27](https://clawhub.ai/user/danlct27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check content before automated posts, external API submissions, web forms, and shared file writes. It helps identify prompt injection, credential leakage, PII exposure, and suspicious instructions before an agent submits content externally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content submitted for review may contain secrets or personal data. <br>
Mitigation: Review the full-content review and logging settings, keep sensitive-data redaction enabled, and limit protected platforms to workflows that need this guard. <br>
Risk: Broad prompt-injection and sensitive-data patterns can pause or reject legitimate submissions. <br>
Mitigation: Tune enabled platforms, severities, timeout, and reject-on-timeout behavior to match the deployment workflow, and require owner approval for high-severity cases. <br>
Risk: Optional shared file-write checks can affect local automation if enabled too broadly. <br>
Mitigation: Enable file-write protection only for shared or public outputs and review the generated configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/danlct27/openclaw-dlp-guard) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces severity labels, owner approval prompts, redacted content previews, and configuration guidance for timeout and platform settings.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
