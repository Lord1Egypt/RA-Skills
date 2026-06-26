## Description: <br>
Scans URLs, domains, and IP addresses for reputation signals and malware or phishing detections using VirusTotal and AbuseIPDB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security analysts, developers, and incident responders use this skill to check submitted URLs, domains, and public IP addresses against reputation and malware/phishing intelligence before deciding whether to monitor, block, or investigate further. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted indicators may include private links, session tokens, private query parameters, internal hostnames, or confidential URLs that are sent to VirusTotal and AbuseIPDB. <br>
Mitigation: Review and sanitize indicators before scanning; remove tokens, private query parameters, internal hostnames, and confidential URLs. <br>
Risk: Broad trigger phrases may cause the skill to run on text that was not intended for external IOC scanning. <br>
Mitigation: Configure the agent so this skill runs only for explicit IOC scan requests. <br>
Risk: External reputation lookups require VirusTotal and AbuseIPDB credentials. <br>
Mitigation: Use dedicated API keys for this skill and rotate them according to the owner's credential-management process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runawaydevil/klaus-ioc-scan) <br>
- [VirusTotal documentation](https://docs.virustotal.com/) <br>
- [VirusTotal API v2 endpoint](https://www.virustotal.com/vtapi/v2) <br>
- [AbuseIPDB API v2 endpoint](https://api.abuseipdb.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text report with risk verdicts, reputation results, links, and action recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIRUSTOTAL_API_KEY and ABUSEIPDB_API_KEY for full external reputation lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
