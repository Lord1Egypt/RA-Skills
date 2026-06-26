## Description: <br>
Memory Association helps an OpenClaw agent recall relevant local memory before starting a task and update memory records after useful decisions, conclusions, or lessons are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxiao-code](https://clawhub.ai/user/wuxiao-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect a new task with prior local memory, project notes, and lessons before spending context on fresh analysis. It also guides when to update daily memory files, project memory, and learning records after completing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally reads and updates local OpenClaw memory and learning files, which may contain sensitive project, client, or personal context. <br>
Mitigation: Review OpenClaw memory and .learnings files for secrets or sensitive data before installation, and use the skill only in workspaces where local memory automation is expected. <br>
Risk: The bundled index-building script can write generated content to local MEMORY_INDEX.md files when run without dry-run mode. <br>
Mitigation: Run the script in dry-run mode first and review the generated index before allowing it to write memory index files. <br>


## Reference(s): <br>
- [Memory Index](references/MEMORY_INDEX.md) <br>
- [Task Association Examples](references/TASK_ASSOCIATION_EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-memory recall guidance and may update OpenClaw memory or learning files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
