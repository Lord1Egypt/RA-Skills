## Description: <br>
Guides agents through parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and related adapter methods in the Hugging Face PEFT ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Desperado991128](https://clawhub.ai/user/Desperado991128) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML engineers use this skill to generate guidance, code snippets, shell commands, and configuration examples for fine-tuning large language models with limited GPU memory. It is most relevant when preparing LoRA or QLoRA adapter training, adapter loading, merging, multi-adapter serving, and PEFT troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes installation and optional source-build examples for ML packages that can affect the user's local Python, CUDA, and GPU environment. <br>
Mitigation: Follow the security guidance to run examples in a virtual environment or container and review package sources before installation. <br>
Risk: The skill uses Hugging Face model and dataset examples that may carry separate access controls, licenses, or data handling obligations. <br>
Mitigation: Review model, dataset, and package sources before use and confirm they are appropriate for the intended fine-tuning workflow. <br>
Risk: The artifact includes examples for pushing merged models or adapters to a hub, which can publish trained artifacts if executed with credentials. <br>
Mitigation: Use push_to_hub only when publication is intentional and the target repository, credentials, and sharing settings have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Desperado991128/peft) <br>
- [PEFT Advanced Usage Guide](references/advanced-usage.md) <br>
- [PEFT Troubleshooting Guide](references/troubleshooting.md) <br>
- [Hugging Face PEFT GitHub Repository](https://github.com/huggingface/peft) <br>
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft) <br>
- [Hugging Face PEFT Models](https://huggingface.co/models?library=peft) <br>
- [LoRA Paper](https://arxiv.org/abs/2106.09685) <br>
- [QLoRA Paper](https://arxiv.org/abs/2305.14314) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, YAML, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation-style guidance for training, saving, merging, serving, and troubleshooting PEFT adapters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
