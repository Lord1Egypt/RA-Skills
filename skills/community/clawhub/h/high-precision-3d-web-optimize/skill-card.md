## Description: <br>
Optimize high-precision .glb/.gltf models for Web 3D and digital twin delivery, including UV-safe simplification, slot-based texture compression, LOD generation, Draco compression, manifest outputs, and browser loading guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neowalker69](https://clawhub.ai/user/neowalker69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D engineers use this skill to prepare high-precision GLB/GLTF assets for Three.js, Babylon.js, digital twin, and Web 3D delivery while preserving UVs, materials, and texture appearance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local model optimization may overwrite or transform source assets in ways that are hard to reverse. <br>
Mitigation: Run the workflow in a dedicated project folder and keep backups of original GLB/GLTF files before processing. <br>
Risk: Unpinned npm dependencies can change optimization output or behavior between runs. <br>
Mitigation: Pin dependency versions before repeated or production use. <br>
Risk: Compression, simplification, or KTX2 loader setup can introduce blur, deformation, decode-path issues, or loading failures. <br>
Mitigation: Validate optimized assets in the target Three.js or Babylon.js viewer and tune texture sizes, LOD ratios, and KTX2 support before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neowalker69/high-precision-3d-web-optimize) <br>
- [Publisher profile](https://clawhub.ai/user/neowalker69) <br>
- [Optimization automation template](artifact/references/optimize-glb.mjs) <br>
- [Three.js LOD loading example](artifact/references/threejs-load-lod.js) <br>
- [Node project package template](artifact/references/package-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code snippets and file-oriented implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of optimized GLB files, LOD GLB files, and manifest JSON through local tooling.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
