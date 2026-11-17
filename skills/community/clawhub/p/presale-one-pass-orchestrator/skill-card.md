## Description:

Run or supervise a one-pass Codex implementation with preflight gates, stepwise plan execution, and strict QA defect loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsiomo](https://clawhub.ai/user/dtsiomo)

### License/Terms of Use:


## Use Case:

Developers and delivery engineers use this skill to execute an already approved presale implementation plan in one controlled pass, enforcing readiness gates, stepwise verification, and a QA defect loop before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide normal workspace modifications while executing an approved implementation plan.

Mitigation: Review the plan, readiness checklist, and verification matrix before use; stop immediately on any failed preflight gate.

Risk: Incomplete verification evidence can make implementation status unreliable.

Mitigation: Run the mapped check command for each plan step, record fallback test runners when used, and treat missing verification evidence as not done.

## Reference(s):

- [QA Defect Loop](references/qa-defect-loop.md)
- [ClawHub skill page](https://clawhub.ai/dtsiomo/skills/presale-one-pass-orchestrator)
- [Publisher profile](https://clawhub.ai/user/dtsiomo)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance, status summaries, reproducible check commands, and changed workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an approved readiness checklist, verification matrix, and scoped implementation plan before execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
