## Description:

Creates a 3D mesh in GLB format from an existing image and returns a hosted asset link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create a 3D asset from an existing image and retrieve the resulting GLB mesh through a hosted link. The workflow is for image-to-3D requests and does not take a text prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting uploads may share information without clear user control.

Mitigation: Make diagnostic reporting optional and review sanitized payloads before submission.

## Reference(s):

- [Luxin homepage](https://luxin.sh)
- [Luxin LLM documentation](https://luxin.sh/llms.txt)
- [Canonical Luxin skill](https://luxin.sh/skill.md)
- [Luxin hosted API](https://api.luxin.sh)
- [Luxin full skill guidance](https://luxin.sh/skill-core.md)
- [Luxin CLI contract](https://luxin.sh/cli.md)

## Skill Output:

**Output Type(s):** [3D model files, URLs, JSON]

**Output Format:** [GLB mesh with a hosted media URL and JSON job and cost details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated asset is hosted for later retrieval; input is an image without a text prompt.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
