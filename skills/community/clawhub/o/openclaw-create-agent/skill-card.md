## Description: <br>
Creates new OpenClaw agents and workspaces through information gathering, workspace construction, system registration, restart verification, and support for human companion and functional agent patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dios-man](https://clawhub.ai/user/dios-man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create, register, verify, and retire OpenClaw agents with consistent workspace files, tool permissions, memory rules, and heartbeat behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local OpenClaw agent configuration and restart or affect gateway behavior. <br>
Mitigation: Review the generated plan first, use the documented dry-run modes, and treat registration, deregistration, and gateway restart steps as administrative actions. <br>
Risk: Created agents may store user profile, preference, and work-context memory. <br>
Mitigation: Disclose memory behavior to affected users or employees and review generated USER.md, MEMORY.md, and memory files before production use. <br>
Risk: Broad tool permissions can increase the impact of a misconfigured generated agent. <br>
Mitigation: Keep alsoAllow permissions minimal and verify requested tools before registration. <br>
Risk: Unexpected workspace paths or identifiers could affect the wrong agent workspace. <br>
Mitigation: Verify agentId and workspace paths remain under ~/.openclaw/agency-agents before writing configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dios-man/openclaw-create-agent) <br>
- [Project repository from metadata](https://github.com/Dios-Man/create-agent) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Workspace File Formats](references/file-formats.md) <br>
- [Human Agent Workspace Path](references/human-path.md) <br>
- [Functional Agent Workspace Path](references/functional-path.md) <br>
- [Bootstrap Protocol](references/bootstrap-protocol.md) <br>
- [Workspace Evolution Rules](references/evolve-rules.md) <br>
- [Memory Rules](references/memory-rules.md) <br>
- [SOUL Writing Guide](references/soul-writing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated workspace/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw workspace files and configuration changes; dry-run modes are available for registration and deregistration scripts.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
