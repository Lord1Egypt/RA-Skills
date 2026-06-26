## Description: <br>
OmniSkill is a universal skill dispatch and execution hub that routes agent tasks, automation events, and plugin execution through a central dispatcher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elohia](https://clawhub.ai/user/elohia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to centralize task routing, plugin registration, and multi-runtime skill execution for local agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad dispatcher that asks agents to route nearly all work through it and can install, register, load, and execute plugins with insufficient scoping. <br>
Mitigation: Install it only when a central plugin dispatcher with broad local authority is intended, and require human review before using automatic onboarding or broad routing behavior. <br>
Risk: Registered plugin paths or metadata can persist and influence future code loading and skill prompt content. <br>
Mitigation: Register only trusted plugin paths and review remote sources before running README commands or adding plugin metadata. <br>
Risk: The socket gateway can expose local execution pathways if bound too broadly. <br>
Mitigation: Keep the gateway bound to localhost and avoid exposing it to untrusted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elohia/omni-skill) <br>
- [OmniSkill architecture and deployment guide](artifact/docs/architecture_and_deployment.md) <br>
- [OmniSkill specification](artifact/docs/spec.md) <br>
- [OmniSkill English README](artifact/README_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style routing guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can propose local CLI commands for packaging, registering, and dispatching plugins.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
