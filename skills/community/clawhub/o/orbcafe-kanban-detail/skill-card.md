## Description: <br>
Build ORBCAFE Kanban boards with CKanbanBoard/CKanbanBucket/CKanbanCard/useKanbanBoard and wire card clicks into DetailInfo using official examples patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenruiyang](https://clawhub.ai/user/shenruiyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement ORBCAFE Kanban workflow boards, controlled drag-and-drop state, and optional DetailInfo navigation from Kanban cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance asks the agent to propose npm package installation commands that can change the target project dependency tree. <br>
Mitigation: Review the listed npm packages and run installation only in the intended project after confirming compatibility. <br>
Risk: The skill depends on an external ORBCAFE module-contracts reference that may be absent from the target workspace. <br>
Mitigation: Confirm the referenced module-contracts file is available before relying on the Hook-first implementation path. <br>
Risk: Generated Kanban or routing code can render a visible UI while drag, state update, or click navigation behavior remains incomplete. <br>
Mitigation: Verify cross-bucket drag, persisted state updates, empty bucket drops, and DetailInfo navigation before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shenruiyang/orbcafe-kanban-detail) <br>
- [Kanban + Detail Guardrails](references/guardrails.md) <br>
- [Kanban + Detail Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript/TSX and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on minimal Hook-first Kanban implementations, verification steps, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
