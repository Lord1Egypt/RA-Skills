## Description:

Manage Hugging Face Hub via hf CLI. Use when working with HF AI models, datasets, spaces, or repos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yevhendiachenko0](https://clawhub.ai/user/yevhendiachenko0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Hugging Face Hub models, datasets, spaces, repositories, jobs, endpoints, discussions, collections, and cache operations through the official hf CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HF_TOKEN can grant access to private Hugging Face resources and write operations when broadly scoped.

Mitigation: Use a read-only token for browsing or downloads, create a separate narrowly scoped write token only when needed, and never expose or log the token value.

Risk: Some hf commands can delete repositories, files, buckets, collections, endpoints, jobs, cache entries, or discussions.

Mitigation: Review destructive hf commands before execution and require explicit user confirmation for delete, prune, cancel, close, merge, or sync-with-delete operations.

## Reference(s):

- [Hugging Face](https://huggingface.co)
- [Hugging Face CLI Guide](https://huggingface.co/docs/huggingface_hub/guides/cli)
- [Hugging Face CLI Reference](https://huggingface.co/docs/huggingface_hub/package_reference/cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires hf CLI and HF_TOKEN for authenticated Hugging Face operations.]

## Skill Version(s):

1.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
