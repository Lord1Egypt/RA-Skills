## Description: <br>
Guides project ideation via Socratic questioning to produce a validated brief before specification when requirements are unclear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and project stakeholders use this skill to clarify unclear project ideas, compare implementation approaches, document decision rationale, and produce a project brief before specification work begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can automatically pass brainstorming context into related skills or subagents and edit planning files without a clear approval checkpoint. <br>
Mitigation: Use --standalone or explicitly tell the agent to stop after brainstorming when you do not want continuation into war-room, specification, or planning-file edits. <br>
Risk: Generated planning documents can carry forward unclear assumptions or incomplete requirements into later phases. <br>
Mitigation: Review the project brief, constraints, selected approach, and acceptance criteria before using the output for implementation planning. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-attune-project-brainstorming) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project brief with structured sections, comparison tables, command snippets, and optional JSON session state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write docs/project-brief.md and .attune/brainstorm-session.json, then continue into related planning or review phases unless the user requests standalone execution.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
