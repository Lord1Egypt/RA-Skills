## Description:

Compare model candidates using weighted metrics and deterministic ranking outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and ML engineers use this skill to rank model candidates from weighted evaluation metrics, generate benchmark leaderboards, and support model promotion decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script writes benchmark output files and may create parent directories or overwrite an existing output path.

Mitigation: Run it in a controlled workspace, choose an explicit output path, and review existing files before execution.

Risk: The dry-run flag is reported in output but does not prevent file creation or overwrite.

Mitigation: Do not rely on --dry-run for side-effect prevention until the script behavior is fixed and re-reviewed.

Risk: CSV exports can carry untrusted model names into spreadsheet software.

Mitigation: Use trusted or reviewed input data and inspect CSV output before opening it in spreadsheet tools.

## Reference(s):

- [Benchmarking Guide](references/benchmarking-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/0x-professor/skills/ml-model-eval-benchmark)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated benchmark artifacts in JSON, Markdown, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a weighted leaderboard, recommended model, applied metric weights, and output artifact path.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
