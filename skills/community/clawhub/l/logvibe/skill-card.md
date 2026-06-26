## Description: <br>
Logvibe colorizes HTTP status codes in log files so developers and system administrators can quickly identify successes, redirects, client errors, and server errors in terminal output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect local or streamed HTTP logs and make status-code classes visually distinguishable while troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The usage examples refer to logvibe.py, while the packaged executable file is tool.py. <br>
Mitigation: Run the packaged tool.py script explicitly or provide a wrapper with the documented name before sharing commands with end users. <br>
Risk: Log files can contain sensitive operational data, and the tool echoes processed log lines to the terminal. <br>
Mitigation: Use the tool only on logs approved for local inspection and avoid sharing terminal output that may contain sensitive values. <br>


## Reference(s): <br>
- [ClawHub Logvibe release page](https://clawhub.ai/albionaiinc-del/logvibe) <br>
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and ANSI-colored terminal text from the tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The packaged tool reads a file path or stdin and prints colorized log lines; it does not write output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
