## Description:

Generates complete Python machine learning experiment pipelines from experiment plan documents, including data preprocessing, model construction, training, evaluation, and result visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhbzx1984](https://clawhub.ai/user/lhbzx1984)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to turn a machine learning paper or experiment plan into a runnable Python training pipeline for PyTorch, TensorFlow, or scikit-learn workflows. It is most appropriate for trusted plans whose generated code will be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted experiment-plan text can become generated executable Python code.

Mitigation: Use trusted plans, inspect generated files, and avoid running generated main.py until plan-derived values are escaped or validated.

Risk: Generated dependencies or pretrained-model calls may install packages or download remote model assets.

Mitigation: Install dependencies in a fresh virtual environment and review requirements and model downloads before execution.

## Reference(s):

- [Data Format Specification](artifact/references/data-format.md)
- [Model Template Reference](artifact/references/model-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/lhbzx1984/skills/paper-to-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated experiment files, including Python modules, requirements.txt, README.md, and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Python is intended to be inspected before installation or execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
