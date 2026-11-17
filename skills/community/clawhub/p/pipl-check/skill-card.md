## Description:

PIPL Check helps compliance teams run a 25-item China PIPL self-assessment with local preview and optional cloud scoring and report generation through compliancehub.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, privacy, and product teams use this skill to preview or run a 25-question assessment against China's Personal Information Protection Law obligations and produce a scored report with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud scoring sends compliance answers and an API key or anonymous trial identifier to compliancehub.cn.

Mitigation: Use the offline non-interactive preview when cloud transfer is not acceptable, and confirm users are comfortable sending answers to compliancehub.cn before scored runs.

Risk: Generated HTML reports are treated by the security evidence as review-worthy if opened in a browser.

Mitigation: Treat HTML reports as untrusted local output and avoid opening or sharing them in higher-risk environments unless reviewed.

Risk: Saved API keys create handling risk on shared systems.

Mitigation: Prefer the COMPLIANCEHUB_API_KEY environment variable over saved key files for CI, shared hosts, and other multi-user environments.

## Reference(s):

- [PIPL Check on ClawHub](https://clawhub.ai/wwumit/skills/pipl-check)
- [ComplianceHub cloud scoring service](https://compliancehub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text with optional HTML or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs send compliance answers to compliancehub.cn; non-interactive preview remains offline.]

## Skill Version(s):

3.0.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
