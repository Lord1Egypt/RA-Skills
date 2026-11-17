## Description:

Hugging Face (huggingface.co). Use this skill for ANY Hugging Face request — searching and reading data. Whenever a task involves Hugging Face, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and inspect Hugging Face models, datasets, Spaces, repositories, endpoints, and the connected user's profile. It can also request chat completions and embeddings through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloads that were not verified in this review, including the oo CLI installer and potentially bundled agent skills.

Mitigation: Review and approve CLI installation separately, and use a pinned, verified release.

Risk: Chat completions and embeddings can be billable inference operations, and requests pass through OOMOL.

Mitigation: Request inference only when intended, agree on input and spending limits, review connection permissions, and avoid sharing sensitive data unless approved.

## Reference(s):

- [Hugging Face](https://huggingface.co)
- [Hugging Face Inference Providers documentation](https://huggingface.co/docs/inference-providers/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; action responses are returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inference actions can incur usage charges; read actions inspect Hugging Face information.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
