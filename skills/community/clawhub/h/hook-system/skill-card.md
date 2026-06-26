## Description: <br>
Hook System lets agents run configurable PreToolUse and PostToolUse hooks to validate inputs, log activity, block execution, and process tool outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhmqq616](https://clawhub.ai/user/xhmqq616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add custom logic before and after tool execution, such as validation, logging, output filtering, and execution blocking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured hooks can read tool inputs, outputs, and environment data. <br>
Mitigation: Use hooks only from trusted sources, review logging behavior, and avoid enabling hooks around tools that handle secrets unless redaction and isolation are in place. <br>
Risk: Hook commands run local shell commands before or after tool execution. <br>
Mitigation: Treat hook commands as trusted code and review each command before installation or configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
