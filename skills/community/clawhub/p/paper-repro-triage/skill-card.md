## Description:

A Chinese paper-reproduction triage workflow that analyzes ML/AI paper evidence, searches or inspects main-paper and dataset source code, locates data-processing code, and prepares Markdown reports or PyTorch reproduction scaffolds when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slight-leaves](https://clawhub.ai/user/slight-leaves)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to assess whether AI papers are reproducible, identify official or local source code and dataset-processing evidence, and prepare a reproduction report or scaffold before any training run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted paper metadata may be written into generated Python or YAML project files.

Mitigation: Review generated files before execution and use safe serialization or repr-style escaping for values derived from paper metadata.

Risk: Clone or output paths may escape the intended workspace if path components contain separators or traversal sequences.

Mitigation: Reject path separators and traversal tokens in paper slugs, bucket names, repository names, and generated output paths before cloning or writing files.

Risk: Generated reproduction projects, cloned repositories, dependencies, datasets, or checkpoints may come from untrusted paper sources.

Mitigation: Run the skill only in a reviewed or sandboxed workspace, and do not install dependencies, download data, run training/evaluation, or load checkpoints until the source and generated code are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slight-leaves/skills/paper-repro-triage)
- [Dataset source tracing workflow](references/dataset-source-tracing.md)
- [No-code reproduction workflow](references/no-code-reproduction.md)
- [Markdown report template](references/output-template.md)
- [Reproducibility rubric](references/reproducibility-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese text summary, Markdown report, generated project files, command candidates, and configuration scaffolds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detailed reports are written under paper-repro-workspace; the skill's automatic phase avoids dependency installation, dataset download, training, evaluation, and inference.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
