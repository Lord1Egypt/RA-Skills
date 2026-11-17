## Description:

Review academic papers for correctness, quality, and novelty using OpenJudge's multi-stage pipeline, supporting PDF files and LaTeX source packages across 10 disciplines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloml0326](https://clawhub.ai/user/helloml0326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and reviewers use this skill to run structured academic paper reviews, correctness checks, criticality assessment, and optional BibTeX verification on PDF or LaTeX paper sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing Python dependencies and running a paper-review pipeline in the user's environment.

Mitigation: Install and run it in an isolated Python environment with pinned, reviewed package versions.

Risk: Paper files, metadata, prompts, or reference information may be sent to selected model providers or reference-checking services.

Mitigation: Provide only the files and API credentials needed for the review, and choose providers appropriate for the paper's confidentiality requirements.

Risk: Model-generated reviews may contain incorrect judgments or miss paper-specific issues.

Mitigation: Treat the review as decision support and require human reviewer validation before relying on scores or correctness findings.

## Reference(s):

- [Paper Review Skill Reference](reference.md)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)
- [OpenAI Models](https://platform.openai.com/docs/models)
- [Anthropic Models](https://docs.anthropic.com/en/docs/about-claude/models)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call model-provider APIs and optional reference-checking services; output can include review scores, correctness findings, criticality assessment, and BibTeX verification summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
