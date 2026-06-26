## Description: <br>
Analyzes BlueKing ITSM ticket exports with field mapping, workload statistics, response-time and trend analysis, frequent issue identification, SLA monitoring, and daily or weekly report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelJochen](https://clawhub.ai/user/MichaelJochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT operations teams and service desk analysts use this skill to analyze exported BlueKing ITSM ticket data, summarize workload and response metrics, identify recurring issues, monitor SLA risk, and generate operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticket exports and generated reports may contain confidential operational or requester information. <br>
Mitigation: Keep ticket files and reports in approved internal locations, redact sensitive fields before sharing, and limit access to authorized service desk or operations personnel. <br>
Risk: Optional API keys or webhook URLs could expose ticket data if configured with broad permissions or unapproved destinations. <br>
Mitigation: Use least-privilege API credentials, store secrets outside shared reports, and configure webhook or scheduled pushes only for approved internal channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MichaelJochen/itsm-ticket-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/MichaelJochen) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON-like analysis summaries, shell command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local CSV or Excel ticket exports and may produce recommendations, report tables, SLA warnings, and operational summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
