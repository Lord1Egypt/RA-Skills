## Description:

Jina AI (jina.ai). Use this skill for ANY Jina AI request — reading, creating, and updating data. Whenever a task involves Jina AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to create embeddings and rerank documents through a connected Jina AI account using the OOMOL oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external CLI installer and exact runtime release are unverified.

Mitigation: Review and verify the CLI and its installation source before allowing installation or execution.

Risk: The CLI workflow may automatically install or change other agent skills.

Mitigation: Check synchronization behavior and disable it if those changes are unwanted.

Risk: Content submitted through the connected workflow may be shared with OOMOL and Jina AI.

Mitigation: Submit only content you intend to share with those services.

## Reference(s):

- [Jina AI](https://jina.ai)
- [Jina AI Reader documentation](https://jina.ai/reader/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Jina AI skill release](https://clawhub.ai/oomol/skills/oo-jina-ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector actions return structured results.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
