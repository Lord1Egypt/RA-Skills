## Description:

Optimizes high-precision GLB/GLTF assets for Web 3D and digital twin delivery with UV-safe simplification, slot-aware texture compression, LOD generation, Draco compression, manifest output, and browser loading guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neowalker69](https://clawhub.ai/user/neowalker69)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D engineers use this skill to prepare large or texture-heavy GLB/GLTF models for browser delivery while preserving UV alignment, material appearance, and practical LOD behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm dependencies may change optimization behavior across installs.

Mitigation: Review and pin dependency versions in a lockfile before production use.

Risk: Automated simplification or texture compression can blur materials, deform geometry, or change color and lighting.

Mitigation: Visually inspect optimized LOD files and tune ratios, texture sizes, color spaces, and compression settings before release.

Risk: KTX2 assets can fail to display if loader support is not initialized for the renderer.

Mitigation: Call KTX2Loader.detectSupport(renderer), verify Draco and KTX2 decoder paths, and test browser loading before deployment.

## Reference(s):

- [optimize-glb.mjs](references/optimize-glb.mjs)
- [threejs-load-lod.js](references/threejs-load-lod.js)
- [package-template.json](references/package-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown response with code snippets, configuration examples, shell commands, and generated asset path summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe optimized GLB outputs, LOD files, manifest settings, browser loading status, and tuning advice.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
