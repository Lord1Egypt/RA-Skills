## Description: <br>
LoRA fine-tuning pipeline for image-generation models on Apple Silicon, with dataset preparation, local training scripts, and comparison image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ML practitioners use this skill to prepare captioned image datasets, train local LoRA adapters, and compare base versus fine-tuned image outputs for custom styles or subjects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads models from Hugging Face and requires an HF_TOKEN. <br>
Mitigation: Use a least-privilege Hugging Face token, review model access and license terms, and run training in an environment where outbound downloads are expected. <br>
Risk: The server security summary notes documentation mismatch: the training script defaults to FLUX.1-schnell while the documentation emphasizes Stable Diffusion, and advertised LLM-as-judge evaluation is not implemented in the artifact. <br>
Mitigation: Set --model_id explicitly before training and add or verify evaluation logic before relying on comparison scores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/lora-finetune) <br>
- [Hugging Face Hub](https://huggingface.co) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash commands and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts can produce LoRA weight files, training logs, generated images, and side-by-side comparison images when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
