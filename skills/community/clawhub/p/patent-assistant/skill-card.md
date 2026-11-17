## Description:

Assists R&D users in turning technical ideas into structured patent disclosure drafts and searching patents for related prior art and novelty analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ty-teo](https://clawhub.ai/user/ty-teo)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and R&D teams use this skill to draft patent technical disclosures, identify missing invention details, run patent searches, compare related results, and prepare next steps for inventor or patent-agent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent search workflows can disclose sensitive invention keywords or unpublished technical details to external search providers.

Mitigation: Use explicit, narrow keywords instead of full confidential disclosures, and review search terms before running provider queries.

Risk: The Innojoy provider uses a plaintext HTTP endpoint, which can expose query contents in transit.

Mitigation: Do not use the Innojoy provider unless plaintext HTTP exposure is acceptable for the information being searched.

Risk: Generated disclosure drafts and novelty analysis are preliminary and may be incomplete or legally insufficient.

Mitigation: Have inventors and qualified patent professionals review drafts, search results, and claim strategy before filing or publication decisions.

## Reference(s):

- [Patent Assistant on ClawHub](https://clawhub.ai/ty-teo/skills/patent-assistant)
- [Publisher profile: ty-teo](https://clawhub.ai/user/ty-teo)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, JSON, and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patent search commands may query external services and can return grouped patent-result summaries with optional similarity scores.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
