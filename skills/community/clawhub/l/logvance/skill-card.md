## Description: <br>
Converts UTC or ISO-formatted timestamps in log files to local system time so developers and system administrators can analyze logs more quickly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use Logvance to convert UTC or ISO timestamps in log files or piped log streams into local time, with optional file output for converted logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input logs may contain sensitive operational or personal data. <br>
Mitigation: Review log contents and handle converted output according to the same data-protection rules used for the original logs. <br>
Risk: The output option writes to the path supplied by the user. <br>
Mitigation: Choose the output path deliberately and avoid overwriting important files. <br>
Risk: Usage examples refer to logvance.py while the shipped script is named tool.py. <br>
Mitigation: Run tool.py as shipped, or rename it consistently before following the examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/logvance) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text log output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read from a log file or stdin and can write converted logs to stdout or a specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
