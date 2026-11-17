## Description:

Provides Hugging Face Hub CLI and Python API guidance for downloading models and datasets, uploading files, managing repositories and Spaces, searching the Hub, and handling cache with HF_TOKEN-backed authentication when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantox](https://clawhub.ai/user/fantox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Hugging Face Hub workflows from an agent, including model and dataset transfer, Hub search, repository administration, Space deployment, and cache inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HF_TOKEN can authorize private reads, uploads, repository deletion, and Space management.

Mitigation: Use fine-grained read-only or repo-scoped tokens by default, and grant write permissions only for the specific workflow that requires them.

Risk: Upload, delete, tag deletion, and --yes commands can modify or remove Hugging Face Hub content without enough guardrails.

Mitigation: Review every write or delete command before execution, and avoid --yes deletion in automation unless an explicit approval step is present.

Risk: Downloads from mutable branches can change over time and affect reproducibility.

Mitigation: Pin downloads to a specific revision or commit SHA for production workflows.

## Reference(s):

- [Hugging Face Hub documentation](https://huggingface.co/docs/huggingface_hub)
- [Hugging Face Hub API Reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated Hugging Face Hub operations that depend on the permissions granted to HF_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
