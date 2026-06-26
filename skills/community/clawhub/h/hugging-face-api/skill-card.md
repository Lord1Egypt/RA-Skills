## Description: <br>
Guides agents to discover Hugging Face models and datasets and use Hugging Face chat or embedding inference with token protection, cost controls, and license checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the Hugging Face Hub, inspect model and dataset metadata, confirm inference support, and run chat or embedding calls while managing token, cost, privacy, and license risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HF_TOKEN exposure can grant access to Hugging Face services. <br>
Mitigation: Use least-privilege tokens from secret storage and never print, log, echo, or place real tokens in shared config. <br>
Risk: Chat or embedding inference may send prompts or document chunks to Hugging Face inference providers. <br>
Mitigation: Avoid confidential or regulated data unless the selected provider is approved for that use. <br>
Risk: Billed inference can create unexpected cost. <br>
Mitigation: Discover for free first, confirm supported models, set max_tokens, batch embeddings, cache repeat work, and require confirmation for expensive calls. <br>
Risk: Model or dataset license terms may restrict downstream use. <br>
Mitigation: Check model and dataset card licenses before commercial use, redistribution, or gated-access workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/hugging-face-api) <br>
- [Hugging Face docs](https://huggingface.co/docs) <br>
- [API and tools reference](artifact/reference/apis-and-tools.md) <br>
- [Models and tasks reference](artifact/reference/models-and-tasks.md) <br>
- [Parameters reference](artifact/reference/parameters.md) <br>
- [Best practices reference](artifact/reference/best-practices.md) <br>
- [Common errors reference](artifact/reference/common-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline JSON and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HF_TOKEN; inference calls may be billed and may send prompts or document chunks to Hugging Face inference providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
