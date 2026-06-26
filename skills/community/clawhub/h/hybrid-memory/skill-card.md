## Description: <br>
Hybrid memory strategy combining OpenClaw's built-in vector memory with Graphiti temporal knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbrunner](https://clawhub.ai/user/clawdbrunner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to decide when to retrieve document-style memory with OpenClaw memory search and when to query temporal facts with Graphiti. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory tools may store personal or project context longer than expected. <br>
Mitigation: Review what facts may be logged, how stored memory can be inspected, and how it can be deleted before setting up Graphiti or sync daemons. <br>
Risk: Memory recall can return incomplete or uncertain past context. <br>
Mitigation: Use the skill's low-confidence pattern: state that memory was checked and avoid presenting uncertain recall as definitive. <br>


## Reference(s): <br>
- [Hybrid Memory on ClawHub](https://clawhub.ai/clawdbrunner/hybrid-memory) <br>
- [OpenClaw Graphiti Memory setup guide](https://github.com/clawdbrunner/openclaw-graphiti-memory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; may guide use of persistent memory tools when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
