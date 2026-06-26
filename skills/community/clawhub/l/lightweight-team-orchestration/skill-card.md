## Description: <br>
Lightweight multi-agent team orchestration with output structure simplified to two folders: agents/ and projects/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to define small multi-agent teams, distribute tasks, and manage versioned deliverables without a complex workflow engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to spawn other agent sessions. <br>
Mitigation: Keep spawned sessions scoped to the intended task and review their prompts and outputs. <br>
Risk: Secrets could be exposed if they are placed in role files or task prompts. <br>
Mitigation: Do not include secrets in SOUL.md files, role definitions, or task distribution prompts. <br>
Risk: Generated project artifacts may contain incorrect or sensitive content. <br>
Mitigation: Review generated artifacts before sharing or using them downstream. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with folder layouts, role-definition examples, and task prompt templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a simple agents/ and projects/ structure with versioned artifact paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
