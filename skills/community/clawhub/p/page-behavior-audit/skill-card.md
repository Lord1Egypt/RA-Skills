## Description: <br>
Deep behavioral audit with hashed policy for page behavior, redirects, response monitoring, screenshots, HAR export, and critical alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Youdaolee](https://clawhub.ai/user/Youdaolee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit approved web pages for redirects, content-policy violations, suspicious XML responses, screenshots, HAR output, and critical WeCom alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill disables browser sandboxing during browser automation. <br>
Mitigation: Run it only in a controlled, hardened browser or container and avoid --no-sandbox where possible. <br>
Risk: The security review says the scan webhook can accept broad URL scans. <br>
Mitigation: Do not expose the webhook publicly and restrict scans to approved targets. <br>
Risk: The security review says screenshots, HAR files, audit logs, and WeCom alerts may contain sensitive data. <br>
Mitigation: Store audit artifacts in a protected directory, limit retention, and treat outbound alerts as sensitive. <br>
Risk: The security review says the package includes an unrelated broad shell-permission file. <br>
Mitigation: Remove or ignore the bundled .claude/settings.local.json before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Youdaolee/page-behavior-audit) <br>
- [Skill homepage](https://github.com/openclaw/page-behavior-audit) <br>
- [Policy verification URL](https://your-org.example.com/policies/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Structured audit results with redirect data, text alerts, response alerts, screenshot paths, HAR paths, and setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECOM_WEBHOOK_URL for critical alerts and may write screenshots, HAR files, and audit logs to OPENCLAW_AUDIT_DIR.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence; artifact metadata declares 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
