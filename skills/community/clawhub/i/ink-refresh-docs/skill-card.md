## Description:

Refresh an existing llms.ink context-pack snapshot and compare source text with its previous version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukax](https://clawhub.ai/user/lukax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to refresh a saved llms.ink context pack from its public source URLs and review heading-level changes against the saved snapshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper supports source collection and dependency discovery beyond the stated refresh workflow, and it was only partially inspected.

Mitigation: Review the helper and any source or manifest inputs before using those workflows; submit only public sources you intend to retrieve.

## Reference(s):

- [llms.ink workflows](https://llms.ink/workflows/)
- [ClawHub skill release](https://clawhub.ai/lukax/skills/ink-refresh-docs)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON context pack and Markdown change report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares 1–5 saved sources by heading and reports added, removed, and updated sections.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
