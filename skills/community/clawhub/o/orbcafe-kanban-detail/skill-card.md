## Description:

Build ORBCAFE Kanban boards with CKanbanBoard/CKanbanBucket/CKanbanCard/useKanbanBoard and wire card clicks into DetailInfo using official examples patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement ORBCAFE Kanban workflow boards, controlled drag-and-drop card movement, and optional Kanban-to-DetailInfo navigation from official example patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing npm dependencies can introduce ordinary supply-chain risk.

Mitigation: Review and pin npm dependencies in the project manifest, use a lockfile or npm ci where possible, and install in a least-privileged development environment.

Risk: A Kanban UI can render while drag, drop, or click behavior has no effect if controlled state or routing requirements are missed.

Mitigation: Use useKanbanBoard with stable bucket and card identifiers, route card clicks from a Client Component, and verify cross-bucket drag, state updates, empty-bucket drops, and DetailInfo navigation.

## Reference(s):

- [Kanban + Detail Guardrails](references/guardrails.md)
- [Kanban + Detail Recipes](references/recipes.md)
- [ClawHub skill page](https://clawhub.ai/shenruiyang/skills/orbcafe-kanban-detail)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript/TSX and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes minimal implementation skeletons, data model guidance, verification steps, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
