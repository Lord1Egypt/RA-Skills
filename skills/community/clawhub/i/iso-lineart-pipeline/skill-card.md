## Description:

Produce isometric line art from a parametric 3D blockout instead of hand-placing polygons in 2D — solid primitives, orthographic projection, z-buffer hidden-line removal with per-sample visibility, stroke weight driven by distance to the silhouette, and a hard minimum feature size so detail survives at game resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT

## Use Case:

Developers and artists can build structurally consistent isometric line-art references from simple 3D primitives, especially for image-to-image workflows or game assets. The scripts render PNG images and can create comparison boards at full size and 240px.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are not fixed, so an installation may resolve to versions with different behavior or advisories.

Mitigation: Pin reviewed NumPy and Pillow versions and check their advisories when updating.

Risk: The sample PNG was excluded from static analysis, leaving its contents unassessed by that scan.

Mitigation: Review the sample image before including or distributing it.

## Reference(s):

- [Line-Art Rules (docs/lineart-rules.md)](docs/lineart-rules.md)
- [ClawHub skill page](https://clawhub.ai/catsmansion/skills/iso-lineart-pipeline)

## Skill Output:

**Output Type(s):** [Image files, Code, Guidance]

**Output Format:** [PNG raster images and Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a comparison board with full-size and 240px views; runs locally without a GPU, network, or API.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
