## Description:

Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for Hugging Face Hub CLI guidance and shell commands for authentication, cache management, model and dataset access, repository operations, Spaces, Jobs, webhooks, buckets, and Inference Endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Hub commands can upload, delete, deploy, schedule jobs, or change repository, Space, webhook, and endpoint state.

Mitigation: Confirm the exact account, namespace, resource name, command target, and destructive flags before any state-changing operation; prefer dry-run or preview options where available.

Risk: Commands that print or pass Hugging Face tokens can expose credentials.

Mitigation: Use least-privilege tokens through environment variables, avoid commands that print token values, and do not include tokens directly in shell history or shared output.

Risk: Installer commands that pipe remote scripts directly into a shell can execute unreviewed code.

Mitigation: Download and inspect installer contents or verify the source independently before executing remote installation scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huggingface/skills/hf-cli)
- [Hugging Face CLI installer](https://hf.co/cli/install.sh)
- [hf-mount GitHub repository](https://github.com/huggingface/hf-mount)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and command reference text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference authenticated Hugging Face Hub operations and should avoid exposing tokens.]

## Skill Version(s):

1.20.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
