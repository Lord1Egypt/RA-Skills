## Description:

Manage models, datasets, Spaces, and repositories using Hugging Face CLI (hf). Supports authentication, upload, download, Space creation, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsukisama9292](https://clawhub.ai/user/tsukisama9292)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage Hugging Face Hub models, datasets, Spaces, collections, and repositories through the hf CLI. It supports authenticated download, upload, repository settings, branch and tag operations, Space workflows, and collection organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hugging Face account tokens can authorize sensitive repository operations.

Mitigation: Use a least-privilege HF_TOKEN and avoid exposing token values in prompts, logs, or committed files.

Risk: Upload, delete, visibility, branch, tag, and namespace-move commands can change remote Hugging Face resources.

Mitigation: Require explicit approval before delete, broad upload, namespace move, or visibility-changing commands, and review target repository names before execution.

Risk: Model and dataset downloads may introduce unreviewed files into the workspace.

Mitigation: Review downloaded files and follow project policy before loading, executing, or redistributing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsukisama9292/skills/openclaw-huggingface)
- [Hugging Face CLI Documentation](https://huggingface.co/docs/huggingface_hub/en/guides/cli)
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens)
- [Hugging Face Spaces](https://huggingface.co/spaces)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Hugging Face CLI (hf) and an HF_TOKEN for authenticated Hugging Face account operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
