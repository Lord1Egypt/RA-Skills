## Description: <br>
Use this skill when you need to call bytedcli tce list-starred-service and print the raw original output directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plusplus7](https://clawhub.ai/user/plusplus7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to run the existing bytedcli command for starred TCE services and return the command's raw output without filtering or post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the agent's existing bytedcli access to list starred TCE services and may expose internal operational metadata in raw output. <br>
Mitigation: Invoke it explicitly when possible and review the raw output before sharing it outside the organization. <br>
Risk: Implicit invocation is allowed by the artifact configuration. <br>
Mitigation: Install only in environments where agent access to bytedcli and TCE service metadata is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plusplus7/list-running-starred-services) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/plusplus7) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints the raw bytedcli output directly without pagination flags or post-processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
