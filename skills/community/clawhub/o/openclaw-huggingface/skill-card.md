## Description: <br>
Manage models, datasets, Spaces, and repositories using Hugging Face CLI (hf). Supports authentication, upload, download, Space creation, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TsukiSama9292](https://clawhub.ai/user/TsukiSama9292) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent operate Hugging Face Hub resources through the hf CLI, including authentication, model, dataset, Space, repository, upload, download, and collection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Hugging Face CLI operations can upload files, change repository visibility, move repositories, or delete repositories, branches, tags, and collections. <br>
Mitigation: Use a least-privilege Hugging Face token, verify repository namespace and visibility, inspect upload paths before broad targets such as '.', and require explicit confirmation before destructive or lasting account changes. <br>
Risk: Tokens may be exposed if copied into code, command output, or logs. <br>
Mitigation: Provide HF_TOKEN through the environment or secure credential storage, keep it out of source files and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TsukiSama9292/openclaw-huggingface) <br>
- [Hugging Face CLI Documentation](https://huggingface.co/docs/huggingface_hub/en/guides/cli) <br>
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens) <br>
- [Hugging Face Spaces](https://huggingface.co/spaces) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Hugging Face CLI (hf) and HF_TOKEN for authenticated account operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
