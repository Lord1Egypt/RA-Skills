## Description: <br>
Hermes Agent Bridge lets an agent delegate prompts to a locally installed Hermes Agent CLI and return the CLI response to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibigbigip](https://clawhub.ai/user/ibigbigip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this bridge when they want OpenClaw to ask a same-system Hermes Agent for a fast, persona-specific answer or task result. The skill is most appropriate when the local Hermes CLI is already trusted and available on PATH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be processed by a separate local agent with its own tools and behavior. <br>
Mitigation: Use the bridge only with a trusted Hermes CLI and avoid sending secrets, private files, or sensitive operational instructions. <br>
Risk: The documented shell invocation passes user prompts through a raw command string. <br>
Mitigation: Prefer explicit user approval and safer non-shell argument passing before using the bridge for sensitive or action-taking work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ibigbigip/hermes-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/ibigbigip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and relayed CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local hermes CLI installation available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
