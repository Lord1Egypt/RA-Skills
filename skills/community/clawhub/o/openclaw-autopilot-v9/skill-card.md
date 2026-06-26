## Description: <br>
Autopilot is a high-autonomy agent mode that proactively plans, executes, follows through, and uses memory-informed context fusion when privacy rules allow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hendr15k](https://clawhub.ai/user/hendr15k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Autopilot when they want an agent to handle open-ended work end to end, including planning, execution, proactive follow-through, memory-aware context use when allowed, and concise status reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables very broad autonomous planning, execution, scheduling, memory access, and persistence behavior. <br>
Mitigation: Install it only when high autonomy is intended, and restrict accessible memory files, directories, scheduling tools, persistent logs, and write scopes before activation. <br>
Risk: Autonomous actions could modify files, create or delete scheduled jobs, store long-term memory, or act on ideas the user did not directly request. <br>
Mitigation: Require explicit confirmation for file modifications, scheduled-job changes, long-term memory writes, and proactive actions outside the user's direct request. <br>
Risk: Memory-informed operation can expose private context if workspace privacy boundaries are not enforced. <br>
Mitigation: Permit memory reads only in contexts where the relevant private or shared memory files are allowed, and block private memory access in shared or group contexts. <br>


## Reference(s): <br>
- [Autonomous Operations](references/autonomous-operations.md) <br>
- [Memory Mining](references/memory-mining.md) <br>
- [Generative Intelligence](references/generative-intelligence.md) <br>
- [Proactivity Catalog](references/proactivity-catalog.md) <br>
- [Editorial Intelligence](references/editorial-intelligence.md) <br>
- [Decision Matrix](references/decision-matrix.md) <br>
- [Strategic Commissioning](references/strategic-commissioning.md) <br>
- [Transparent Execution](references/transparent-execution.md) <br>
- [Capability Building](references/capability-building.md) <br>
- [Creative Engine](references/creative-engine.md) <br>
- [Error Recovery](references/error-recovery.md) <br>
- [Slash Commands](references/slash-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, and file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; concrete outputs depend on the user's task and available agent tools.] <br>

## Skill Version(s): <br>
9.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
