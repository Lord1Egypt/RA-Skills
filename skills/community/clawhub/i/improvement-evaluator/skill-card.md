## Description:

Improvement Evaluator measures whether skill changes improve AI task performance by running YAML task suites, judging task outputs, and reporting execution pass-rate deltas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to compare candidate SKILL.md changes against a baseline on predefined task suites before promotion or gating. It is useful when execution pass rate matters more than document structure scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real evaluations may send local SKILL.md content and task prompts to the Claude CLI.

Mitigation: Use --mock for local testing, and run non-mock evaluations only in a sandbox or disposable workspace with reviewed inputs.

Risk: Untrusted ranking artifacts or task suites may point evaluation at unintended skill paths.

Mitigation: Review and constrain target paths to real SKILL.md files before running the evaluator.

Risk: Task suites with weak baselines or broad prompts can produce misleading pass-rate signals.

Mitigation: Validate suites before use, require a sane baseline pass rate, and prefer focused tasks with deterministic judges where possible.

## Reference(s):

- [Task Suite Format](artifact/references/task-format.md)
- [Writing Effective Task Suites](artifact/references/writing-tasks-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/improvement-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON evaluation artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evaluation artifacts include execution_pass_rate, baseline_pass_rate, delta, verdict, per-task results, and a truth_anchor path.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
