## Description: <br>
Adds memory trust validation rules for OpenClaw 4.2 so an agent verifies stale or decision-relevant memory before acting on it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicshliu](https://clawhub.ai/user/nicshliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to add a prompt-level validation workflow for OpenClaw memory before changing code, making decisions, or sending messages based on remembered files, functions, or configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes persistent OpenClaw agent behavior through system prompt configuration. <br>
Mitigation: Review the exact prompt text before adding it to OpenClaw configuration. <br>
Risk: The validation workflow may run local file and text searches for paths or symbols mentioned in memory. <br>
Mitigation: Limit checks to paths and symbols relevant to the current workspace and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicshliu/openclaw-trust-validation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-level rules intended for OpenClaw system prompt configuration] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
