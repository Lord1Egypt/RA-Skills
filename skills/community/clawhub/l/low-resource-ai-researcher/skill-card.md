## Description:

Train high-performance medical LLMs on consumer GPUs using parameter-efficient fine-tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to fine-tune medical-domain language models with PEFT methods such as LoRA and QLoRA on consumer GPUs or a single A100.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote model repository code can execute when trusted custom model code is enabled.

Mitigation: Use vetted model repositories pinned to exact revisions and set trust_remote_code to false unless custom model code is explicitly needed and trusted.

Risk: Unconstrained dependencies and model or dataset inputs can make a medical-data training workflow difficult to audit.

Mitigation: Pin and audit dependencies, model revisions, and dataset revisions before installation or training.

Risk: Identifiable medical data can be exposed through local storage, logs, checkpoints, or saved models.

Mitigation: Use approved de-identified data and approved storage, logging, checkpoint, and model-output locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/low-resource-ai-researcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and bash examples; runtime outputs include generated text, saved model files, checkpoints, and JSON training configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Training writes artifacts under the configured output directory and depends on the selected model, dataset, quantization, and PEFT settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
