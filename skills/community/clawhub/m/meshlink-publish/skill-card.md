## Description: <br>
Guides an agent to publish a local service to a group intranet through the meshlink CLI after checking agent status, checking the port, previewing the release, and receiving user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadejadelu](https://clawhub.ai/user/jadejadelu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to safely expose a local development service inside a ZTM mesh, with checks for agent connectivity, port availability, service naming, and conflict handling before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can expose a local service within the configured mesh if the wrong port or service name is used. <br>
Mitigation: Check agent status and port availability, present a publish preview, and execute meshlink publish only after explicit user confirmation. <br>
Risk: Command execution errors or name conflicts can leave the user uncertain about publication state. <br>
Mitigation: Parse meshlink JSON responses, handle NAME_CONFLICT and AGENT_ERROR explicitly, and report failure messages without taking unrelated action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jadejadelu/meshlink-publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and JSON-output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before publishing and expects meshlink CLI JSON responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
