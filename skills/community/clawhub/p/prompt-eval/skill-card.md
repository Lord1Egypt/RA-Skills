## Description: <br>
Evaluates and improves a supplied prompt through a structured pipeline for test planning, case generation, prompt execution, scoring, reporting, and validation-gated iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rivin-dong](https://clawhub.ai/user/rivin-dong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and evaluation reviewers use this skill to benchmark, score, diagnose, and improve prompts using CSV-first evidence artifacts and a final optimized prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rivin-dong/prompt-eval) <br>
- [JSON Schema & CSV Format Reference](references/json_schema.md) <br>
- [Evaluator Prompt Guide](references/prompt_b_guide.md) <br>
- [Test Plan Guide](references/test_plan_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and reports with CSV and JSON evaluation artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates user-confirmed local output directories and CSV-first evaluation records; prompts, test data, adversarial cases, and model outputs should be treated as untrusted data with minimal retention.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
