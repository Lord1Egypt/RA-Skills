## Description:

模型蒸馏大师 helps developers transfer capabilities from a large teacher model into a smaller student model through analysis, synthetic data generation, QLoRA training, evaluation, and deployment packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to plan and run model distillation workflows for edge deployment, API cost reduction, domain-specific smaller models, or faster inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install software, download models, run training, and execute generated scripts.

Mitigation: Use an isolated virtual environment or container, pin dependencies and model revisions, and require explicit approval before package installs, downloads, training, or generated script execution.

Risk: Model loading and teacher-model workflows can expose users to unreviewed remote code or remote API data handling.

Mitigation: Disable trust_remote_code unless the model repository has been reviewed, and avoid sensitive or regulated datasets with remote teacher APIs unless provider privacy and retention terms are confirmed.

## Reference(s):

- [Model Distillation Methodology](artifact/references/methodology.md)
- [Knowledge Distillation Original Paper](https://arxiv.org/abs/1503.02531)
- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)
- [Gemma Documentation](https://ai.google.dev/gemma)
- [ModelScope Gemma 3 4B IT Repository](https://www.modelscope.cn/LLM-Research/gemma-3-4b-it.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/YAML configuration and Python/shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow plans, generated training and evaluation scripts, reports, and deployment packaging instructions for model distillation.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.yaml, and CHANGELOG dated 2024-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
