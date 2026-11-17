## Description:

Discover, evaluate, and run Hugging Face models, datasets, and spaces with license checks, benchmark prompts, and reproducible integration plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to discover, compare, evaluate, and run Hugging Face models, datasets, and Spaces for a concrete task. It helps move from catalog browsing to license-aware shortlist selection, repeatable benchmarking, and integration-ready inference plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search command placeholders can execute unintended local shell syntax if untrusted search text is pasted directly into command templates.

Mitigation: URL-encode search terms or use structured HTTP tooling before running discovery commands.

Risk: Selected search terms, filter inputs, model IDs, and inference payloads may be sent to Hugging Face services.

Mitigation: Send only task-relevant inputs and avoid private, unrelated, or regulated data unless the user has approved that transfer.

Risk: HF_TOKEN may be exposed through logs, notes, or transcripts during hosted inference setup.

Mitigation: Keep tokens in environment variables or secret storage and never copy full token values into memory files or conversation logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/hugging-face)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Hugging Face Models API](https://huggingface.co/api/models)
- [Hugging Face Datasets API](https://huggingface.co/api/datasets)
- [Hugging Face Spaces API](https://huggingface.co/api/spaces)
- [Hugging Face Inference API](https://api-inference.huggingface.co/models/{model_id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, scoring rubrics, setup steps, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local memory files under ~/hugging-face/ and Hugging Face API calls that require HF_TOKEN for hosted inference.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
