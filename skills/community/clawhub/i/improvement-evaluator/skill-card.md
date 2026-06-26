## Description: <br>
Improvement Evaluator runs predefined task suites against candidate and baseline skills, judges each task output, and reports execution pass-rate metrics for gating decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to test whether a skill change improves real task execution, compare candidate and baseline pass rates, and feed execution deltas into quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execution-based evaluations run task suites through Claude and may run pytest-based judges on generated output. <br>
Mitigation: Install only when execution evaluation is intended, review task suites and fixtures before use, and run pytest-based judges in a sandbox when fixtures are not fully trusted. <br>
Risk: Candidate skills, task prompts, or outputs may contain secrets or private customer data during evaluation. <br>
Mitigation: Avoid placing secrets or private customer data in candidate skills or prompts, and use mock mode for dry runs when live execution is unnecessary. <br>


## Reference(s): <br>
- [Task Suite Format](artifact/references/task-format.md) <br>
- [Writing Effective Task Suites](artifact/references/writing-tasks-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/improvement-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON evaluation artifact with Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports execution_pass_rate, baseline_pass_rate, delta, verdict, per-task results, and an audit path; mock mode supports dry runs without live model execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
