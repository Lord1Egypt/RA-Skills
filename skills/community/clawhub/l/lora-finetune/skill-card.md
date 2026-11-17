## Description:

LoRA fine-tuning helper for image generation models on Apple Silicon, covering dataset setup, local training, and comparison image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and creative engineers use this skill to prepare image-caption datasets, run local LoRA training on Mac hardware, and generate base-versus-adapter comparison images for custom visual styles or characters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads unpinned models from Hugging Face using a Hugging Face token.

Mitigation: Use a read-only token, verify or pin model repositories before running, and run the training code in a controlled local environment.

Risk: The documentation and scripts materially differ: the training script defaults to FLUX while the documentation describes Stable Diffusion and LLM scoring that is not implemented.

Mitigation: Review the scripts before use, choose the intended model explicitly, and treat documented evaluation scores as illustrative unless reproduced with separate evaluation tooling.

## Reference(s):

- [Lora Finetune on ClawHub](https://clawhub.ai/nissan/skills/lora-finetune)
- [Hugging Face Hub](https://huggingface.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and Python scripts that create LoRA weights, logs, and comparison images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and HF_TOKEN; downloads base models from Hugging Face while training runs locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
