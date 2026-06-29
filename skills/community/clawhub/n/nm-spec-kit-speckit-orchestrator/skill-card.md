## Description: <br>
Orchestrates Spec Driven Development by coordinating spec, plan, and task skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate Speckit-style specification, planning, task generation, implementation, and verification workflows across `/speckit-*` command phases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words may cause the skill to activate during general planning requests. <br>
Mitigation: Invoke or enable it around explicit `/speckit-*` workflows and confirm the current task is Spec Driven Development before following its coordination guidance. <br>
Risk: Workflow guidance can produce or update specification, plan, task, and checklist artifacts that later steer implementation. <br>
Mitigation: Review generated artifacts for project fit, consistency, and unresolved blockers before using them to guide code changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-spec-kit-speckit-orchestrator) <br>
- [Project homepage from release metadata](https://github.com/athola/claude-night-market/tree/master/plugins/spec-kit) <br>
- [Command-skill matrix](modules/command-skill-matrix.md) <br>
- [Artifact structure](modules/artifact-structure.md) <br>
- [Progress tracking](modules/progress-tracking.md) <br>
- [Writing-plans extensions](modules/writing-plans-extensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command mappings, progress checklists, artifact structure, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; release security evidence reports no executable code, credential handling, or hidden data movement.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
