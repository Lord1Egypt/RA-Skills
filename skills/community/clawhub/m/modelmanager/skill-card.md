## Description: <br>
OpenClaw model management skill for viewing, setting, and managing the large language models used by OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamxxu](https://clawhub.ai/user/williamxxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect available models, check current model status, set a default model, and manage fallback models. Mutating operations are intended only after explicit user instruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted model IDs can lead to unintended local command execution. <br>
Mitigation: Use only trusted, simple model IDs shown by the model list, avoid arbitrary or pasted model strings, and update the implementation to call subprocess without a shell and validate model IDs. <br>
Risk: Changing the default or fallback model can alter OpenClaw behavior, costs, or service availability. <br>
Mitigation: Run mutating commands only after explicit user instruction and review the selected model before applying the change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamxxu/modelmanager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local OpenClaw model-management commands and reports command output or errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
