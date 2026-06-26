## Description: <br>
Runs long or continuous shell commands with file-backed logs, truncated previews, and fast log scanning. Invoke when shell output may be large, ongoing, or hard to inspect directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qipengguo](https://clawhub.ai/user/qipengguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run long-running, continuous, or high-volume shell commands while monitoring compact status cards instead of reading raw full output. It is useful for builds, log followers, failure scans, and timestamp-focused inspection of large command logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run real shell commands, including commands that may alter files or system state. <br>
Mitigation: Review commands before execution and require explicit approval for destructive, privileged, reboot, disk-formatting, or file-deletion operations. <br>
Risk: Command output is written to local log files that may contain private paths, tokens, or other sensitive data. <br>
Mitigation: Avoid sending secrets to command output and clean temporary logs when command output may include sensitive information. <br>
Risk: Background or continuous sessions can keep running after the immediate task is finished. <br>
Mitigation: Use the stop workflow for continuous commands and check session status before ending the debugging loop. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qipengguo/long-context-shell) <br>
- [Publisher profile](https://clawhub.ai/user/qipengguo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Structured status text with truncated log previews, scan matches, session identifiers, and log paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are compact by default and point to file-backed logs for deeper inspection.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
