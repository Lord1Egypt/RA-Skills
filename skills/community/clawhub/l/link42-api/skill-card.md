## Description:

Helps agents use authorized LINK42 models for text, vision, embeddings, images, and video, including cost estimates, owned assets, and asynchronous task recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomas202301](https://clawhub.ai/user/thomas202301)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other LINK42 users can discover models available to their key, plan and estimate requests, and carry out authorized text, vision, image, video, embedding, and owned-asset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A LINK42 key may grant access to usage data or paid API operations.

Mitigation: Use only a key intended for this skill, review its usage-read permission, and keep the key private.

Risk: Generation, scoring, uploads, cancellation, or asset deletion may incur charges or change owned resources.

Mitigation: Run these actions only on explicit user request after confirming cost and scope; estimate paid generation first when possible.

## Reference(s):

- [LINK42 API skill on ClawHub](https://clawhub.ai/thomas202301/skills/link42-api)
- [API operations](artifact/references/api-operations.md)
- [Request examples](artifact/references/request-examples.md)
- [Tool integration](artifact/references/tool-integration.md)
- [Capability map and workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, Media links]

**Output Format:** [Text or Markdown with commands, structured results, and links to generated media when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, identifiers, and known costs when available.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
