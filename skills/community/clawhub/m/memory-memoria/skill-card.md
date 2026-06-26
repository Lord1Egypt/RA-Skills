## Description: <br>
Use Memoria as OpenClaw's durable memory slot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[randomradio](https://clawhub.ai/user/randomradio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route durable memory tasks to Memoria, including storing reusable facts, retrieving prior context, correcting or forgetting memory, and managing snapshots or branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory can persist and later reuse personal or project context. <br>
Mitigation: Store only durable, reusable information; avoid secrets or highly sensitive personal data; periodically review, correct, forget, or purge stored memories. <br>
Risk: Memory setup may require database, API, and embedding-provider credentials. <br>
Mitigation: Verify the external Memoria plugin source and use dedicated credentials before enabling the memory plugin. <br>
Risk: Bulk memory deletion or major rewrites can remove useful context. <br>
Mitigation: Create a snapshot before risky memory maintenance, then verify retrieval or list results after changes. <br>


## Reference(s): <br>
- [Memory Slot Operations](references/operations.md) <br>
- [Usage Patterns](references/patterns.md) <br>
- [OpenClaw Setup](references/setup.md) <br>
- [Tool Surface](references/tool-surface.md) <br>
- [Memoria Homepage](https://github.com/matrixorigin/Memoria) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and tool-selection guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on explicit memory writes, retrieval, correction, deletion, snapshots, rollback, branches, and maintenance workflows.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
