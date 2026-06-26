## Description: <br>
让 AI Agent 拥有自我反思和元认知能力——知道自己正在做什么、做得怎么样、承诺了什么、需要改进什么。包含自我状态记录、承诺追踪和定期反思机制。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilozhao](https://clawhub.ai/user/lilozhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add self-reflection routines, promise tracking, heartbeat checks, and workspace state templates to an OpenClaw-compatible agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent self-state and user-relationship notes, which can accumulate sensitive personal details without clear consent, retention, or deletion controls. <br>
Mitigation: Install only with explicit opt-in; review SELF_STATE.md, MEMORY.md, SOUL.md, and AGENTS.md before use; avoid sensitive personal details; define review, expiration, and deletion rules. <br>
Risk: The helper script reads a fixed workspace SELF_STATE.md path and prints status fields that may contain personal or operational context. <br>
Mitigation: Run the script only in the intended OpenClaw workspace and avoid sending its output to shared logs unless the state file has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilozhao/metacognition-skill) <br>
- [Publisher profile](https://clawhub.ai/user/lilozhao) <br>
- [Skill homepage](https://gitee.com/lilozhao/carbon-silicon-bond-protocol) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [SELF_STATE.md template](templates/SELF_STATE.md) <br>
- [HEARTBEAT.md template](templates/HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell snippets and workspace state templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces files and instructions for SELF_STATE.md, HEARTBEAT.md, MEMORY.md, SOUL.md, and AGENTS.md; no API keys were detected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
