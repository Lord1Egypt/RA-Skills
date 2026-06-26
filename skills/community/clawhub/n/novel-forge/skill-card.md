## Description: <br>
Long-form novel workflow for creating, continuing, resuming, and repairing serialized fiction with externalized project state, role-to-model mapping, worldbuilding, character sheets, full outlines, 10-chapter batch outlines, style sampling, chapter drafting, consistency review, memory tracking, and spawned multi-session collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[228998098](https://clawhub.ai/user/228998098) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and developers use this skill to manage long-running fiction projects, including project setup, continuation, recovery from truncated drafts, canon planning, chapter drafting, review, and persistent story memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local OpenClaw model inventory and writes story state and chapter files into a project directory. <br>
Mitigation: Use it in a dedicated project workspace and review created or modified project files before relying on them as canon. <br>
Risk: In multi-agent mode, selected story context may be sent to spawned model sessions. <br>
Mitigation: Confirm the role-to-model mapping before canon work and keep task packets limited to the smallest relevant story context. <br>
Risk: Long-running fiction state can accumulate stale canon, style drift, or unresolved plot conflicts. <br>
Mitigation: Use the included checkpoints, reviewer stage, memory updates, and batch-outline invalidation rules before continuing chapters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/228998098/novel-forge) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Runbook](artifact/references/runbook.md) <br>
- [Schemas](artifact/references/schemas.md) <br>
- [State Machine](artifact/references/state-machine.md) <br>
- [Main Session Constraints](artifact/references/main-session-constraints.md) <br>
- [Continuation Checklist](artifact/references/continuation-checklist.md) <br>
- [Prompts](artifact/references/prompts.md) <br>
- [Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON project state, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates file-backed novel project state, canon files, chapter drafts, review notes, memory updates, and role-to-model mapping guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
