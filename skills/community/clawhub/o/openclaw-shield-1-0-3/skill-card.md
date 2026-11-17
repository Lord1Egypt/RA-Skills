## Description:

OpenClaw Shield helps agents guide setup and use of an external security scanner for AI-agent code, including static threat checks, optional runtime guard configuration, ClamAV integration, alerting, and audit reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run or plan AI-agent security scans, review JSON findings, and configure defensive controls such as allowlists, output sanitization, audit logs, and malware-signature checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to clone and run an external repository that is not pinned by the server-resolved release evidence.

Mitigation: Review the external repository source, pin it to a trusted commit, and record the exact revision before executing scanner or deployment commands.

Risk: Daily cron scans and runtime guard setup can create recurring execution, file access, network controls, alerting destinations, and operational changes outside the reviewed package.

Mitigation: Do not enable scheduled scans or runtime protection until scripts, permissions, allowlists, alert routing, logging behavior, and disable or removal steps are documented and approved.

Risk: Security scanner output can include false positives or incomplete detections because pattern-based scanning does not replace human security review.

Mitigation: Treat generated reports as triage input, review flagged code manually, and validate any remediation before deployment.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/kenswj/skills/openclaw-shield-1-0-3)
- [OpenClaw Shield external repository](https://github.com/pfaria32/OpenClaw-Shield-Security)
- [Resonant shield inspiration](https://github.com/ManoloRemiddi/resonantos-open-system-toolkit/blob/main/BUILD_YOUR_OWN_SHIELD.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON report references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference scanner-generated JSON reports, policy allowlists, cron schedules, alerting setup, and audit log review.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
