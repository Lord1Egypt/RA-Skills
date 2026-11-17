## Description:

Cohere (cohere.com). Use this skill for ANY Cohere request — reading, creating, and updating data. Whenever a task involves Cohere, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Cohere users can use this agent skill to request Cohere chat responses, create text embeddings, and rerank documents through an already connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes changeable remote code, and its dependency may install persistent skills into other agent applications.

Mitigation: Review the CLI installation, use a verified release, inspect any additional skills it installs, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Content sent through the connected account is processed by OOMOL and Cohere.

Mitigation: Send only content that the user has authorized OOMOL and Cohere to process.

## Reference(s):

- [Cohere API reference](https://docs.cohere.com/reference/about)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Cohere](https://cohere.com)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell command and JSON examples; connector responses are JSON and may contain generated text, embeddings, or ranked documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by Cohere action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
