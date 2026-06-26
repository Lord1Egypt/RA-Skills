## Description: <br>
Validates executed improvement candidates with a six-layer quality gate and routes outcomes to keep, reject, revert, or pending human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill inside an improvement pipeline to validate completed changes, create auditable gate receipts, and route higher-risk candidates for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local files during rollback when gate.py processes execution artifacts. <br>
Mitigation: Run it only in a trusted improvement pipeline, use trusted ranking and execution artifacts, and verify rollback pointers before execution. <br>
Risk: Broad triggers could activate the skill outside the intended quality-gate workflow. <br>
Mitigation: Narrow triggers before broad publishing or installation, and invoke the skill only for completed improvement candidates that require gate validation. <br>
Risk: State and review records may affect project workflow decisions if shared across unrelated projects. <br>
Mitigation: Keep the state root project-scoped and review pending approvals before promotion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/improvement-gate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON receipt outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces gate decisions, per-layer results, rollback status, and pending-review records when applicable.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
