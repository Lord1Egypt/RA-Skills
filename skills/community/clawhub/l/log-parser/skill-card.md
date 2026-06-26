## Description: <br>
Parse and analyze various log formats (nginx, apache, syslog, application logs). Extract key information and generate reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeter226](https://clawhub.ai/user/freeter226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps teams, and security operators use this skill to parse local nginx, apache, syslog, and JSON application logs, then generate statistics, filters, top values, and error-focused reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed samples and reports can expose secrets, personal data, or operational details already present in the selected log file. <br>
Mitigation: Use the parser only on logs you intend to inspect, redact sensitive logs when needed, and avoid sharing generated JSON reports without review. <br>
Risk: The tool reads local files by path and may process the wrong log if invoked with an unintended file argument. <br>
Mitigation: Check the target path before execution and run it in a workspace with access limited to the logs needed for the analysis. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/freeter226/log-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from a local Python command-line tool, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected local log file and supports sample or result limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
