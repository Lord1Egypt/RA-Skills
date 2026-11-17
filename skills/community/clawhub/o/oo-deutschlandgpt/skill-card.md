## Description:

Use this skill to work with DeutschlandGPT through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other DeutschlandGPT users can use the connected OOMOL account to create chat completions, generate embeddings, and list available models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs review because it automatically falls back to running an unverified online installer and labels text-generation requests as reads.

Mitigation: Review the CLI separately before enabling the skill; treat chat and embedding calls as external processing, send only intended text, and set spending limits.

## Reference(s):

- [DeutschlandGPT Platform API documentation](https://docs.deutschlandgpt.de/platform-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [DeutschlandGPT homepage](https://www.deutschlandgpt.de/)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls]

**Output Format:** [Text or JSON responses, including embedding vectors and model lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected DeutschlandGPT action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
