## Description:

Generates an interactive 3D spatiotemporal HTML map from JSON milestone data, positioning nodes by geography and year with hover detail cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooof](https://clawhub.ai/user/ooof)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn milestone datasets into interactive timeline-map web pages for domains such as AI, automotive, semiconductors, pharma, or internet history. The skill is most useful when each milestone has year, location, latitude, longitude, type, title, and description fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated web pages may trust unescaped input fields when built from unreviewed JSON.

Mitigation: Use controlled or carefully reviewed input data and sanitize fields before publishing generated pages.

Risk: Remote or private asset URLs can be fetched and embedded during page generation.

Mitigation: Avoid third-party datasets and private remote asset URLs unless they have been reviewed and approved.

Risk: Generated pages load Three.js dependencies from unpkg unless the dependencies are bundled locally.

Mitigation: Bundle or otherwise approve the runtime dependencies before deployment in restricted or public environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ooof/skills/industry-evolution-3d)
- [3D Industry-Evolution Graph Lessons](artifact/references/lessons.md)
- [AI History Sample Dataset](artifact/examples/ai_history_sample.json)

## Skill Output:

**Output Type(s):** [code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; generated artifact is an HTML file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages inline configured image and map assets, but load Three.js from unpkg unless dependencies are bundled locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
