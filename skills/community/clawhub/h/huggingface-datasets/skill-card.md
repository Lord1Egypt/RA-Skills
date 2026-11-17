## Description:

Provides Hugging Face Dataset Viewer API workflows for fetching subset and split metadata, paginating rows, searching text, applying filters, retrieving parquet URLs, and reading dataset size or statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to inspect Hugging Face datasets through Dataset Viewer endpoints, including split discovery, row previews, pagination, search, filtering, parquet URL lookup, and dataset metadata checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upload workflows could send local agent session history, prompts, file paths, tool outputs, secrets, or PII to Hugging Face.

Mitigation: Use the read-only Dataset Viewer endpoints unless uploads are explicitly required; stage, review, and redact files before upload, and do not upload whole session directories.

Risk: Hugging Face CLI uploads require credentials and could broaden exposure if run with an unreviewed toolchain or over-broad token.

Mitigation: Use a pinned or preinstalled Hugging Face CLI and a narrowly scoped token for intended uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huggingface/skills/huggingface-datasets)
- [Hugging Face Dataset Viewer API](https://datasets-server.huggingface.co)
- [Hugging Face new dataset page](https://huggingface.co/new-dataset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API endpoint examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Dataset Viewer API guidance is the primary output; upload examples require explicit user intent and credential handling.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
