## Description:

Use Gemini through an OOMOL-connected account for Gemini requests to read, create, and update data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use the OOMOL-connected Gemini service to generate content, create embeddings, count tokens, list models, and manage video generation operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run remote installer code and may add skills to other agent applications; the live installers were not inspected.

Mitigation: Review and approve CLI installation separately, verify the installer and release, and disable startup skill synchronization if only Gemini access is needed.

Risk: Gemini requests pass through OOMOL as an intermediary, which may handle confidential content.

Mitigation: Consider OOMOL's handling of confidential content before sending it through the service.

## Reference(s):

- [Gemini API documentation](https://ai.google.dev/gemini-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Embeddings, Image and video links, Shell commands]

**Output Format:** [JSON action results and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media may be returned as transit URLs.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
