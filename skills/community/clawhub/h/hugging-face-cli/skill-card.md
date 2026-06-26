## Description: <br>
Manage Hugging Face Hub via hf CLI. Use when working with HF AI models, datasets, spaces, or repos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YevhenDiachenko0](https://clawhub.ai/user/YevhenDiachenko0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for Hugging Face Hub CLI guidance, including installing the `hf` command, authenticating with `HF_TOKEN`, browsing models, datasets, spaces, papers, and managing Hub resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can delete repositories, files, buckets, collections, endpoints, discussions, jobs, or local cache data. <br>
Mitigation: Require explicit user confirmation before destructive `hf` commands or commands using deletion flags. <br>
Risk: Hugging Face access tokens can grant read or write access to private Hub resources. <br>
Mitigation: Use `HF_TOKEN` from the environment, never print or persist the token value, and prefer read tokens unless write operations are required. <br>
Risk: Uploads to public repositories may expose sensitive files or model weights. <br>
Mitigation: Warn the user before public uploads and confirm the target repository visibility and content. <br>


## Reference(s): <br>
- [Hugging Face](https://huggingface.co) <br>
- [Hugging Face CLI installation guide](https://huggingface.co/docs/huggingface_hub/guides/cli#getting-started) <br>
- [Hugging Face CLI guide](https://huggingface.co/docs/huggingface_hub/guides/cli) <br>
- [Hugging Face CLI reference](https://huggingface.co/docs/huggingface_hub/package_reference/cli) <br>
- [Hugging Face token settings](https://huggingface.co/settings/tokens) <br>
- [ClawHub skill page](https://clawhub.ai/YevhenDiachenko0/hugging-face-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-confirmed commands for Hugging Face Hub operations; should not expose or log `HF_TOKEN`.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
