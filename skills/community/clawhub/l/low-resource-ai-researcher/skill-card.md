## Description: <br>
Train high-performance medical LLMs on consumer GPUs using parameter-efficient fine-tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to configure and run parameter-efficient fine-tuning for medical-domain LLMs on constrained GPU hardware. It supports LoRA and QLoRA workflows for medical QA, diagnosis, and clinical-note style tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable trusted remote model code, which may execute code from model repositories. <br>
Mitigation: Disable trust_remote_code unless a vetted model requires it, and use trusted model repositories. <br>
Risk: Broad unpinned machine learning dependencies can change behavior or increase supply-chain exposure. <br>
Mitigation: Install in an isolated environment, pin dependency versions, and review dependencies before use. <br>
Risk: Medical training data can contain identifiable patient information or regulated data. <br>
Mitigation: Do not train on identifiable patient data without authorization and controls for datasets, logs, checkpoints, and generated outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/low-resource-ai-researcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; training runs can write model files and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce model checkpoints, tokenizer files, adapter weights, generated text, and training configuration under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
