## Description: <br>
Permission Guard describes a layered permission model for agent command execution, including dangerous-command blocking, rule-priority handling, auto-mode allowlists, denial tracking, and sensitive-information checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinnzen](https://clawhub.ai/user/sinnzen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to design or review permission checks before an agent runs shell commands, changes files, makes network requests, installs dependencies, pushes code, or performs privileged operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-allow or 'don't ask again' rules can permit commands without sufficient review. <br>
Mitigation: Require explicit approval before saving broad command permissions and review how future implementations persist permission rules. <br>
Risk: Bypass mode removes confirmation checks and can allow sensitive operations to proceed unchecked. <br>
Mitigation: Keep bypass mode disabled outside tests and prefer ask or auto modes for normal use. <br>
Risk: Permission guidance can be implemented inconsistently, especially for dangerous commands, network pipe execution, and secrets in command strings. <br>
Mitigation: Preserve explicit deny rules for dangerous command patterns, network pipe execution, and sensitive-information detection when adapting this guidance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON snippets, TypeScript-style examples, and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install code, run commands, or export data by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
