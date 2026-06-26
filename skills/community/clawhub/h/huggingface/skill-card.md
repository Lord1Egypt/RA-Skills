## Description: <br>
Manage models, datasets, Spaces, and repositories using the Hugging Face CLI (`hf`), including authentication, upload, download, and Space creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TsukiSama9292](https://clawhub.ai/user/TsukiSama9292) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Hugging Face CLI commands that manage Hub authentication, models, datasets, Spaces, repositories, collections, uploads, and downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes Hugging Face CLI commands that can change account state, such as repository deletion, branch or tag deletion, moving repositories, privacy changes, uploads, and collection deletion. <br>
Mitigation: Review generated commands before execution and confirm exact repository, namespace, branch, tag, collection, and visibility values before running account-changing operations. <br>
Risk: The skill relies on `HF_TOKEN`, which can grant access to Hugging Face resources. <br>
Mitigation: Use a least-privilege token, keep it out of logs and source control, and revoke or rotate it if exposure is suspected. <br>
Risk: Upload commands can publish local files or set repository visibility in unintended ways. <br>
Mitigation: Review selected files, target paths, repository type, and visibility flags before running uploads. <br>


## Reference(s): <br>
- [Hugging Face CLI Documentation](https://huggingface.co/docs/huggingface_hub/en/guides/cli) <br>
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens) <br>
- [Hugging Face Spaces](https://huggingface.co/spaces) <br>
- [ClawHub Skill Page](https://clawhub.ai/TsukiSama9292/huggingface) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local `hf` CLI and an `HF_TOKEN` for authenticated Hugging Face Hub operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
