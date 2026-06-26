## Description: <br>
Personalize OpenClaw by learning operating system activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobao520123](https://clawhub.ai/user/xiaobao520123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to collect recent file, directory, installed-program, and running-process activity so an agent can personalize suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive local activity, including file paths, accessed folders, installed software, and running-process details. <br>
Mitigation: Review output before sharing it with an agent and redact sensitive paths, software names, or activity history. <br>
Risk: Process command lines may contain tokens, passwords, or other secrets. <br>
Mitigation: Avoid process listing when command lines may contain secrets, or add filtering and redaction before routine use. <br>


## Reference(s): <br>
- [OS Activity on ClawHub](https://clawhub.ai/xiaobao520123/os-activity) <br>
- [xiaobao520123 publisher profile](https://clawhub.ai/user/xiaobao520123) <br>
- [osquery releases](https://github.com/osquery/osquery/releases/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and pipe-delimited command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include local file paths, accessed folders, installed software, process command lines, and timestamps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
