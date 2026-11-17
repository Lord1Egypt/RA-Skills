## Description:

Generates vintage-style historical map images from GeoJSON data with configurable projections, palettes, timelines, decorative elements, and post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muxueqingze](https://clawhub.ai/user/muxueqingze)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, educators, developers, and agents use this skill to turn historical GeoJSON basemaps and optional texture or event inputs into map images for articles, videos, blogs, and educational material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted GeoJSON, event JSON, basemap images, or parchment textures may affect local processing behavior or resource use.

Mitigation: Install and run the skill in an isolated Python environment, and process only GeoJSON, JSON, and image files from trusted sources.

Risk: Extremely large basemap or parchment images can consume significant memory and CPU during cropping, resizing, and post-processing.

Mitigation: Use runtime memory and CPU limits, and downsample large texture inputs before generation.

Risk: Historical boundaries may be approximate or contain regional gaps, which can make generated maps unsuitable for publication without review.

Mitigation: Review the source GeoJSON boundary precision, manually edit important regions, or use commercial data for publication-quality maps.

## Reference(s):

- [ClawHub Historical Map Skill](https://clawhub.ai/muxueqingze/skills/historical-map)
- [historical-basemaps Data Source](https://github.com/aourednik/historical-basemaps)
- [Publisher Profile](https://clawhub.ai/user/muxueqingze)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash and Python examples; generated output is a PNG image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on provided GeoJSON, optional event JSON, optional texture images, projection, palette, region, and DPI settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
