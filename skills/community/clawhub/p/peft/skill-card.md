## Description:

Guides developers through parameter-efficient fine-tuning for LLMs with LoRA, QLoRA, and adapter workflows in the Hugging Face PEFT ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desperado991128](https://clawhub.ai/user/desperado991128)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to fine-tune large language models with limited GPU memory, configure LoRA and QLoRA adapters, merge or serve adapters, and troubleshoot PEFT training issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes package installation and optional source compilation steps that can introduce supply-chain or environment risk.

Mitigation: Use a virtual environment or container, avoid administrator privileges, and pin dependencies for production use.

Risk: Adapter or merged-model publishing can expose licensed, private, or sensitive model artifacts.

Mitigation: Publish to Hugging Face Hub only after verifying permissions, license terms, and data-sensitivity requirements.

## Reference(s):

- [PEFT Advanced Usage Guide](references/advanced-usage.md)
- [PEFT Troubleshooting Guide](references/troubleshooting.md)
- [Hugging Face PEFT documentation](https://huggingface.co/docs/peft)
- [Hugging Face PEFT repository](https://github.com/huggingface/peft)
- [PEFT models on Hugging Face](https://huggingface.co/models?library=peft)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, Bash, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation commands, PEFT configuration examples, training recipes, adapter workflows, and troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
