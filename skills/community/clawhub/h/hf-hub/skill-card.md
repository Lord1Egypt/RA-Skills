## Description: <br>
Access Hugging Face Hub models, datasets, and spaces via the huggingface_hub Python library. Use when you need to list, search, download, or upload HF assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noesis-boss](https://clawhub.ai/user/noesis-boss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to browse Hugging Face Hub models, datasets, and spaces, inspect model or dataset metadata, and move files to or from Hub repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Hugging Face token to access private resources or upload files. <br>
Mitigation: Use a least-privilege HF token from the platform secret store and verify repository ownership, visibility, and target paths before upload. <br>
Risk: Uploads may expose secrets, private datasets, regulated data, or files intended to remain local. <br>
Mitigation: Review local paths and repository settings before upload, and do not upload sensitive data unless the repository and token permissions are appropriate. <br>


## Reference(s): <br>
- [Hugging Face token settings](https://huggingface.co/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with local downloaded files or Hugging Face Hub upload results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HF_TOKEN from the environment or platform secret store when authenticated Hub access is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
