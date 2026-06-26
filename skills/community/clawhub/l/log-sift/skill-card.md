## Description: <br>
Log Sift filters large log files by keywords and date ranges from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and support engineers use Log Sift to narrow large logs to relevant time windows or matching keywords during troubleshooting and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads whichever local log file or stdin stream the user provides, which may contain sensitive data. <br>
Mitigation: Run it only on logs you are authorized to inspect and avoid exposing sensitive output in shared terminals or transcripts. <br>
Risk: The artifact provides a Python script but no installer or wrapper. <br>
Mitigation: Run tool.py directly or create a reviewed wrapper before relying on a log_sift command in automation. <br>


## Reference(s): <br>
- [Log Sift on ClawHub](https://clawhub.ai/albionaiinc-del/log-sift) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints matching log lines from a selected file or stdin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
