## Description: <br>
Protects against prompt injection attacks by sanitizing, validating, and securely processing untrusted external content from websites, emails, and documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackworm](https://clawhub.ai/user/blackworm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to sanitize and validate untrusted web, email, document, command, and file-path content before passing it into an agent workflow or acting on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts background update behavior and keeps persistent learned state. <br>
Mitigation: Review the learning and update configuration before installation; disable learning and auto-updates unless they are explicitly needed. <br>
Risk: Non-strict processing can make enforcement decisions ambiguous after threat detection. <br>
Mitigation: Use strictMode for enforcement paths and treat detected threats as blocking unless a reviewer explicitly approves the content. <br>
Risk: fetchAndSecureContent is not evidence of complete real web sanitization. <br>
Mitigation: Do not rely on fetchAndSecureContent alone; process fetched content through reviewed sanitization and validation steps before use. <br>
Risk: Alert callbacks may expose raw prompts, documents, commands, paths, or matched threat text in logs. <br>
Mitigation: Redact or suppress sensitive alert payload fields before logging, storing, or forwarding alerts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blackworm/prompt-injection-protection) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Security enhancements summary](artifact/SECURITY_ENHANCEMENTS_SUMMARY.md) <br>
- [Auto-learning security summary](artifact/AUTO_LEARNING_SECURITY_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript integration examples and structured JavaScript API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce sanitized content, threat analysis results, alert payloads, safe-or-unsafe decisions, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
