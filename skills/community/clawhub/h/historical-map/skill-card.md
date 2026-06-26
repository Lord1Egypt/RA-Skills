## Description: <br>
Generate beautiful vintage-style historical maps from GeoJSON data with multiple projections, color palettes, timelines, compass roses, parchment overlays, and vignette effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muxueqingze](https://clawhub.ai/user/muxueqingze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, history bloggers, educators, and developers use this skill to generate vintage-style historical map images from local GeoJSON data for articles, videos, lessons, and agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill adds Python geospatial and image-processing dependencies. <br>
Mitigation: Install only in an environment where the listed packages are acceptable and review dependency versions before deployment. <br>
Risk: Local GeoJSON, event JSON, basemap, and texture files determine what the renderer reads and what appears in generated maps. <br>
Mitigation: Use trusted local input files, inspect paths before running commands, and validate map data accuracy for publication-quality output. <br>


## Reference(s): <br>
- [Historical Map on ClawHub](https://clawhub.ai/muxueqingze/historical-map) <br>
- [historical-basemaps data source](https://github.com/aourednik/historical-basemaps) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Python code snippets; generated artifacts are PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local GeoJSON data and optional local event, basemap, or texture files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
