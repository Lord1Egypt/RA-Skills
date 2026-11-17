## Description:

Test agents or models against predefined test cases to validate model routing, performance, and output quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandorocker](https://clawhub.ai/user/nandorocker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeatable OpenClaw agent or model tests, compare requested versus actual model routing, and capture performance and output-quality results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs OpenClaw CLI commands and sends predefined benchmark prompts to selected agents or models.

Mitigation: Run it only in an OpenClaw environment where the selected agent or model is intended to receive the bundled test prompts.

Risk: The skill tails OpenClaw logs to infer model routing, token usage, and runtime metrics.

Mitigation: Use it where log access is appropriate and rely on the documented structured fields rather than arbitrary log content.

Risk: A caller-controlled --out path can write a JSON report to disk.

Mitigation: Provide --out only with an output path that is intended to be created or overwritten.

## Reference(s):

- [Bundled test cases](references/test-cases.json)
- [ClawHub skill page](https://clawhub.ai/nandorocker/skills/model-tester)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON report with a short plain-text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write the JSON report to a caller-specified output path with --out.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
