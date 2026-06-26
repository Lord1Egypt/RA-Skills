## Description: <br>
Full Hugging Face Hub skill for CLI and Python API workflows, including downloading models and datasets, uploading files, managing repositories and Spaces, searching the Hub, and handling cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantox](https://clawhub.ai/user/fantox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate Hugging Face Hub operations for model inference preparation, dataset pipelines, repository management, and Space deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HF_TOKEN may grant access to private or gated Hugging Face resources and write operations. <br>
Mitigation: Use the narrowest token scope possible, prefer read-only or repo-scoped tokens, and never hard-code tokens in scripts. <br>
Risk: Upload, delete, cache cleanup, and Space-management commands can change or remove remote or local resources. <br>
Mitigation: Review target repository names, repo types, revisions, and delete or cleanup prompts before execution. <br>
Risk: Remote inference or Hub operations may send prompts, audio, files, or metadata to network services. <br>
Mitigation: Avoid sending private prompts, audio, or sensitive artifacts unless the user has approved the destination and data handling. <br>


## Reference(s): <br>
- [Hugging Face Hub documentation](https://huggingface.co/docs/huggingface_hub) <br>
- [Hugging Face Hub API reference](artifact/references/api_reference.md) <br>
- [Hugging Face access tokens](https://huggingface.co/settings/tokens) <br>
- [ClawHub skill page](https://clawhub.ai/fantox/huggingface-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fantox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated Hugging Face Hub operations that depend on HF_TOKEN scope and network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
