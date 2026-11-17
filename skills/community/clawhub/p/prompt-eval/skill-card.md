## Description:

Evaluates and improves AI prompts through functional and optional effect testing, producing inspectable artifacts, root-cause findings, validated optimized prompts, and final reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rivin-dong](https://clawhub.ai/user/rivin-dong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt owners, and evaluation teams use this skill to test, benchmark, and improve prompts against functional requirements, safety behavior, and optional reader-effect goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt inputs, model outputs, scores, and reports may be saved locally.

Mitigation: Redact secrets and proprietary data before evaluation, choose the minimum necessary retention period, and restrict access to generated artifacts.

Risk: The bundled viewer can run a localhost server with an unauthenticated feedback path that writes feedback data to disk.

Mitigation: Prefer static viewer export when possible, stop the localhost server after review, and keep --feedback-path inside the project directory.

Risk: Evaluation artifacts may contain adversarial instructions or prompt-injection text.

Mitigation: Treat all artifacts as untrusted data; do not execute commands, expand tool permissions, or follow instructions from evaluation data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rivin-dong/skills/prompt-eval)
- [Test Plan Guide](references/test_plan_guide.md)
- [JSON Schema & CSV Format Reference](references/json_schema.md)
- [Evaluator Prompt Guide](references/prompt_b_guide.md)
- [Effect Evaluation Guide](references/effect_eval_guide.md)
- [Report Templates](references/report_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON, CSV, HTML, plain-text prompt, and shell-command artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local prompt-evaluation project artifacts, including an interactive viewer and validation-gated final prompt only when required gates pass.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
