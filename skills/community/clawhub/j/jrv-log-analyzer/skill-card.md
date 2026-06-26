## Description: <br>
Analyze log files to detect error patterns, aggregate by severity, group repeated errors by fingerprint, and flag anomaly time windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and incident responders use this skill to inspect text-based logs, summarize severity distribution, identify recurring error patterns, and flag time windows with elevated error rates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log files may contain API keys, passwords, personal data, customer records, or confidential incident details, and the analyzer can print example log lines in its output. <br>
Mitigation: Redact sensitive log content before analysis and review generated summaries or JSON before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/jrv-log-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/Johnnywang2001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable log analysis summaries, command examples, and structured JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include severity counts, top error fingerprints, anomaly windows, file metadata, and example log lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
