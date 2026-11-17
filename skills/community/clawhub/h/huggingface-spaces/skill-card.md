## Description:

Build, deploy, and maintain applications on Hugging Face Spaces across Gradio, Docker, Static SDKs, ZeroGPU, dedicated hardware, model loading, debugging, buckets, inference providers, and community grants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, deploy, debug, and maintain Hugging Face Spaces, including Gradio apps, ZeroGPU deployments, static or Docker Spaces, persistent storage, and provider-backed demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to create public Spaces, attach paid hardware, use paid buckets, or post grant discussions on the user's behalf.

Mitigation: Require explicit user confirmation before creating public resources, enabling paid hardware or storage, changing visibility, or posting community grant requests.

Risk: The skill may involve Hugging Face tokens, secrets, OAuth, or gated model access.

Mitigation: Use scoped tokens only when necessary, store sensitive values as Space secrets rather than public environment variables, and avoid logging or exposing credentials.

Risk: Generated Spaces may install or run unverified third-party code, Git dependencies, or direct wheel URLs.

Mitigation: Review source repositories before use, pin Git dependencies to reviewed commits, prefer verified package sources, and add hashes for direct wheel artifacts where practical.

Risk: Dev mode and SSH troubleshooting can introduce weak access controls if configured casually.

Mitigation: Use dev mode and SSH only as a last resort, prefer passphrase-protected SSH keys, and disable or rotate access after troubleshooting.

## Reference(s):

- [Hugging Face Spaces skill page](https://clawhub.ai/huggingface/skills/huggingface-spaces)
- [Hugging Face publisher profile](https://clawhub.ai/user/huggingface)
- [Hugging Face Spaces overview](https://huggingface.co/docs/hub/spaces-overview)
- [Spaces Docker SDK](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Spaces Static SDK](https://huggingface.co/docs/hub/spaces-sdks-static)
- [Spaces configuration reference](https://huggingface.co/docs/hub/spaces-config-reference)
- [ZeroGPU documentation](https://huggingface.co/docs/hub/spaces-zerogpu)
- [Storage Buckets documentation](https://huggingface.co/docs/hub/storage-buckets)
- [Persistent storage with Buckets](references/buckets.md)
- [Debugging and iteration](references/debugging.md)
- [Gradio for Spaces](references/gradio.md)
- [Community GPU grants](references/grants.md)
- [Inference Providers](references/inference-providers.md)
- [Known errors](references/known-errors.md)
- [requirements.txt for Spaces](references/requirements.md)
- [ZeroGPU](references/zerogpu.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands and configuration snippets for Hugging Face CLI, Space README frontmatter, Python apps, requirements files, secrets, hardware settings, logs, smoke tests, buckets, grants, and provider-backed deployments.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
