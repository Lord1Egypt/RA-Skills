## Description: <br>
Coordinates an end-to-end skill improvement pipeline that proposes, scores, optionally evaluates, executes, and gates low-risk changes with retry feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent skill to run a full improvement cycle over one or more skills, including proposal generation, scoring, optional evaluation, execution, gate decisions, and retry traces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify files in the selected target skill. <br>
Mitigation: Run it first on a test copy or tightly scoped --target, keep --state-root isolated, and review generated diffs, receipts, traces, and backups before trusting kept changes. <br>
Risk: Accepted proposals could still add incorrect or misleading guidance to documentation or guardrail files. <br>
Mitigation: Review gate receipts and scan the modified skill before deployment; use task suites where available to add evaluator evidence. <br>
Risk: The current implementation only auto-keeps a narrow class of low-risk Markdown changes and may skip deeper evaluation when no task suite is provided. <br>
Mitigation: Treat pending, rejected, and reverted candidates as review signals, and provide a task suite when higher-confidence evaluation is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/improvement-orchestrator) <br>
- [Architecture](references/architecture.md) <br>
- [Guardrails](references/guardrails.md) <br>
- [Phases](references/phases.md) <br>
- [Adapters](references/adapters.md) <br>
- [Skill-Evaluator Adapter](references/skill-evaluator-adapter.md) <br>
- [End-to-End Demo](references/end-to-end-demo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON artifacts] <br>
**Output Format:** [Markdown guidance with shell commands and machine-readable JSON artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local run state, receipts, diffs, traces, and backups under the chosen state directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
