## Description:

Scans URLs, domains, and IP addresses for reputation signals and malware or phishing detections using VirusTotal and AbuseIPDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

Security analysts, developers, and incident responders use this skill to triage URLs, domains, and public IP addresses by checking third-party reputation data and receiving a concise verdict with recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full URLs submitted for reputation checks may disclose sensitive paths, query strings, tokens, or internal resources to third-party services.

Mitigation: Use only approved indicators, strip secrets or customer data before scanning, and add an explicit confirmation or lookup-only mode before operational use.

Risk: Results depend on external API availability, API keys, rate limits, and third-party reputation data quality.

Mitigation: Treat the verdict as triage support, confirm high-impact decisions with additional investigation, and monitor API errors or missing data.

## Reference(s):

- [VirusTotal Documentation](https://docs.virustotal.com/)
- [AbuseIPDB API v2](https://api.abuseipdb.com/api/v2)
- [ClawHub Skill Page](https://clawhub.ai/runawaydevil/skills/klaus-ioc-scan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with summary verdicts, quick result tables, detailed IOC reports, and recommended actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIRUSTOTAL_API_KEY and ABUSEIPDB_API_KEY for full results.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
