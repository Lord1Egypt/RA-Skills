## Description: <br>
Analyze server logs for error patterns, IP frequency, time-based analysis, and alert generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolaoqi](https://clawhub.ai/user/laolaoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and operations teams use this skill to inspect syslog, custom log files, or piped log streams for recurring errors, IP frequency patterns, time buckets, and spikes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided trace or log material may include sensitive cookies, tokens, request bodies, console logs, DOM content, screenshots, attachments, or operational details. <br>
Mitigation: Redact sensitive data and limit shared inputs and outputs before using or distributing analysis results. <br>
Risk: System logs may require elevated access, and large files can expose more data than intended. <br>
Mitigation: Run the analysis with the least required permissions and pre-filter or reduce large log files before analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laolaoqi/laolaoqi-log-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/laolaoqi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with tabular summaries and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports error counts, top matching messages, hourly or daily buckets, IPv4 frequency, and spike indicators when the input format supports them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
