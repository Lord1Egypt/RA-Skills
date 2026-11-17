## Description:

Converts selected elements from an HTML file into individual high-resolution PNG images with configurable selector, dimensions, and output directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiker1996](https://clawhub.ai/user/shiker1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to render page-like HTML sections into PNG assets for previews, social posts, documentation, or image pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renders caller-supplied HTML in a browser with network access.

Mitigation: Render only trusted HTML or run the skill in a tightly isolated environment with minimal filesystem access and restricted network egress.

Risk: The legacy conversion script deletes a hard-coded output directory recursively before rendering.

Mitigation: Prefer the configurable Agent Skill entry point and avoid the legacy script unless the hard-coded path has been reviewed.

Risk: The release depends on Puppeteer and lockfile dependencies that may age over time.

Mitigation: Update Puppeteer and lockfile dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiker1996/skills/html-pages-to-images)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PNG image files plus a JSON-compatible execution result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns image paths, image count, and output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
