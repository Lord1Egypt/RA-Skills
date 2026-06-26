## Description: <br>
Control Adobe Photoshop from the shell via Flue - ExtendScript bridges without an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative production users use this skill to let an agent inspect Photoshop document state and make bounded, user-directed edits through Flue's local shell bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to automate Photoshop or another supported desktop application. <br>
Mitigation: Use it only for applications and documents the user intends the agent to inspect or modify. <br>
Risk: Setup requires installing a local bridge dependency. <br>
Mitigation: Review Flue before approving setup and require explicit user approval before installing or running setup commands. <br>
Risk: Desktop automation can make unintended document changes. <br>
Mitigation: Prefer small, inspectable steps and avoid destructive actions unless the user explicitly requests them. <br>


## Reference(s): <br>
- [Photoshop skill page](https://clawhub.ai/sfkislev/photoshop) <br>
- [Flue GitHub project](https://github.com/SFKislev/flue) <br>
- [Flue PyPI package](https://pypi.org/project/flue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets; Flue bridge execution returns structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before installing or setting up Flue.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
