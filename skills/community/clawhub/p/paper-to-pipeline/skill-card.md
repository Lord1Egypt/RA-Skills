## Description: <br>
Generates runnable machine learning and deep learning experiment pipelines from an uploaded experiment plan, including data preprocessing, model code, training, evaluation, and visualization components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhbzx1984](https://clawhub.ai/user/lhbzx1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and machine learning engineers use this skill to turn experiment planning documents into structured Python project files for PyTorch, TensorFlow, or scikit-learn workflows. It is intended for local code generation that users review before running. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated experiment code may contain incorrect assumptions or unsafe defaults for the user's dataset, model, or environment. <br>
Mitigation: Review the generated Python, configuration, and dependency files before running them. <br>
Risk: Running a generated project may install packages or download pretrained models. <br>
Mitigation: Use a new empty output directory and an isolated environment before executing generated commands or code. <br>


## Reference(s): <br>
- [Data Format Specification](references/data-format.md) <br>
- [Model Template Reference](references/model-templates.md) <br>
- [ClawHub release page](https://clawhub.ai/lhbzx1984/paper-to-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/lhbzx1984) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, configuration, guidance] <br>
**Output Format:** [Generated Python project files with Markdown documentation and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local experiment project structure; generated code should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
