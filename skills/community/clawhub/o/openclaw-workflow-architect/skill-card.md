## Description:

Helps developers design, review, and generate OpenClaw workflows by choosing the right boundary between Lobster deterministic execution and OpenProse AI orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thanh01pmt](https://clawhub.ai/user/thanh01pmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide whether workflow steps belong in Lobster or OpenProse, review existing workflow files for layering anti-patterns, and generate .lobster or .prose workflow structures with approval and compatibility guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval-gate examples can read a caller-supplied local file path.

Mitigation: Constrain approval-gate file inputs to approved workspace or artifact directories and reject absolute paths or traversal before execution.

Risk: Setup guidance may use mutable npm or npx package installs.

Mitigation: Pin package versions and review resolved package metadata before installing in shared or production environments.

Risk: Workflow templates may send lesson or business content to llm-task.

Mitigation: Do not process confidential content through llm-task unless the selected external model path is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thanh01pmt/skills/openclaw-workflow-architect)
- [Layering guide](artifact/references/layering-guide.md)
- [Lobster specification](artifact/references/lobster-spec.md)
- [OpenProse specification](artifact/references/openprose-spec.md)
- [Curriculum pipeline example](artifact/references/examples/curriculum-pipeline.md)
- [Approval gate example](artifact/references/examples/gate-approval.md)
- [Lesson worker example](artifact/references/examples/lesson-worker.md)
- [OpenClaw Lobster documentation](https://docs.openclaw.ai/tools/lobster)
- [OpenClaw Prose documentation](https://docs.openclaw.ai/prose)
- [Prose](https://www.prose.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and generated workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .lobster and .prose workflow files, compatibility notes, review findings, and approval-gate checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
