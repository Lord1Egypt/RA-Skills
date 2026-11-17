## Description:

Deep behavioral audit with hashed policy (CSP-compliant, no plaintext badwords)

This skill is ready for commercial/non-commercial use.

## Publisher:

[youdaolee](https://clawhub.ai/user/youdaolee)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to audit web pages for redirects, content policy violations, response anomalies, screenshots, HAR captures, and critical findings alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-driven page audits and webhook access can be high impact if exposed to untrusted callers.

Mitigation: Install only in a controlled environment, do not expose the webhook to untrusted callers, and restrict outbound and internal network access for the browser.

Risk: Screenshots and HAR exports may retain sensitive page data.

Mitigation: Avoid auditing authenticated or sensitive pages unless screenshot and HAR retention in OPENCLAW_AUDIT_DIR is acceptable.

Risk: Unsafe defaults and elevated installation paths can increase blast radius.

Mitigation: Remove --no-sandbox before processing untrusted pages, pin installer versions, and avoid optional sudo/system installation until the exact installed files are reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youdaolee/skills/page-behavior-audit)
- [ClawHub Publisher Profile](https://clawhub.ai/user/youdaolee)

## Skill Output:

**Output Type(s):** [text, files, configuration]

**Output Format:** [JSON-like audit report with paths to screenshot and HAR artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WECOM_WEBHOOK_URL for critical alerts; OPENCLAW_AUDIT_DIR controls retained audit files.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact metadata reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
