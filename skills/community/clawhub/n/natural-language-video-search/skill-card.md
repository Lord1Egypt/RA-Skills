## Description:

Semantic search over video files using Gemini embeddings to index dashcam, security camera, or mp4 footage and find and auto-trim matching clips from natural language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssrajadh](https://clawhub.ai/user/ssrajadh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to index local video footage, search it with natural language, and extract matching clips. It is especially relevant for dashcam, security camera, surveillance, and Tesla footage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs mutable external code and dependencies from the sentrysearch repository.

Mitigation: Review the external repository before installation, use a dedicated environment, and pin a known commit where possible.

Risk: Video indexing can process sensitive footage through the Gemini API.

Mitigation: Limit indexed folders to intended footage and avoid sensitive videos unless API processing is acceptable.

Risk: Generated clips or Tesla overlays may expose GPS, location, speed, or other telemetry.

Mitigation: Review trimmed clips and overlays before sharing them outside the intended audience.

## Reference(s):

- [sentrysearch homepage](https://github.com/ssrajadh/sentrysearch)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local video clips through the referenced sentrysearch commands.]

## Skill Version(s):

0.2.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
