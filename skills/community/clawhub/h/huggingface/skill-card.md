## Description:

Manage models, datasets, Spaces, and repositories using Hugging Face CLI (hf). Supports authentication, upload, download, Space creation, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsukisama9292](https://clawhub.ai/user/tsukisama9292)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask an agent for Hugging Face CLI guidance and command examples for authentication, model and dataset discovery, repository management, file transfer, Spaces, and collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hugging Face tokens can grant access to private models, datasets, Spaces, or account actions if exposed or over-scoped.

Mitigation: Use a least-privilege token, keep `HF_TOKEN` out of prompts and logs, and rotate the token if exposure is suspected.

Risk: Upload commands can publish unintended files or expose data when broad paths such as `.` are used.

Mitigation: Review local paths before upload, prefer explicit file paths, and verify repository visibility before publishing.

Risk: Repository delete, branch delete, tag delete, move, or visibility changes can be destructive.

Mitigation: Require user confirmation before delete, move, or visibility-changing operations.

## Reference(s):

- [Hugging Face CLI Documentation](https://huggingface.co/docs/huggingface_hub/en/guides/cli)
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [ClawHub Skill Page](https://clawhub.ai/tsukisama9292/skills/huggingface)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Hugging Face CLI (`hf`) and a Hugging Face token available as `HF_TOKEN` or supplied through supported CLI authentication.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
