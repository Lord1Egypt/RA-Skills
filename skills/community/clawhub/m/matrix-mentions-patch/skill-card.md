## Description: <br>
Fixes an OpenClaw Matrix plugin mention detection bug where a missing agent ID prevents configured group-room @mentions from being recognized. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw Matrix gateways use this skill to identify and manually apply a targeted source edit that restores @mention detection in configured group rooms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the edit to the wrong Matrix extension file or with the wrong agent ID can leave mention detection broken. <br>
Mitigation: Verify the target file and actual agent ID before editing, and keep the original line available for rollback. <br>
Risk: Restarting the OpenClaw gateway can briefly interrupt service. <br>
Mitigation: Restart the gateway only when a short interruption is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code snippets and a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable payload.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
