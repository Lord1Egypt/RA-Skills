## Description: <br>
Hermes 与本地 OpenClaw 协同工作 — 模型互调、记忆共享、任务分工 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate Hermes with a local OpenClaw workspace for model calls, shared memory, task delegation, and ClawHub publishing handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad persistent workspace state sharing and delegated publishing authority between Hermes and OpenClaw. <br>
Mitigation: Install only for intentional collaboration workflows, inspect referenced local scripts first, restrict writes to a dedicated collaboration folder, and require explicit human approval before publishing or sending tasks that can change accounts, files, or public content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fish1981bimmer/openclaw-collab) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local command examples for OpenClaw and Hermes collaboration workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
