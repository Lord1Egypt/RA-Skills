## Description: <br>
Run evidence-gated coding sprints with frozen ACs, separated builder/verifier roles, and durable proof artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use Proof Loop to run coding sprints where acceptance criteria are frozen before implementation, verifier work is separated from builder work, and completion is gated by durable proof artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper commands can create or update repo-local task artifacts. <br>
Mitigation: Confirm the repository root and task id before running helpers, and use dry-run mode before writing harness guidance files. <br>
Risk: Existing harness guide files can be overwritten when force options are used. <br>
Mitigation: Use --force only when intentionally replacing an existing guide file. <br>


## Reference(s): <br>
- [Proof Loop Workflow](references/workflow.md) <br>
- [Artifact Schemas](references/artifacts.md) <br>
- [Agent Brief Template](references/brief-template.md) <br>
- [Loopsmith Bridge](references/loopsmith-bridge.md) <br>
- [Proof Loop ClawHub Page](https://clawhub.ai/leostehlik/proof-loop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, JSON verdict artifacts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and checks repo-local proof artifacts under .agent/tasks/<TASK_ID>/ when its helpers are run.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
