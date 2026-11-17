## Description:

Perplexity (perplexity.ai). Use this skill for ANY Perplexity request — reading, creating, and updating data. Whenever a task involves Perplexity, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through their connected OOMOL account to search Perplexity, create Sonar chat completions, list available models, and generate embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup provides remote CLI install commands, including a shell command that executes a downloaded installer.

Mitigation: Review and approve the CLI installation separately; prefer a fixed, verified release instead of executing the supplied remote-script command directly.

Risk: Requests pass through OOMOL and may incur charges.

Mitigation: Check applicable OOMOL and Perplexity billing or credit status before making chargeable requests.

## Reference(s):

- [Perplexity API documentation](https://docs.perplexity.ai/)
- [Perplexity](https://www.perplexity.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-perplexity)

## Skill Output:

**Output Type(s):** [Text, JSON, Vector embeddings]

**Output Format:** [Generated text and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Embedding actions return vector data; available models and response fields depend on Perplexity.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
