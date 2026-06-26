## Description: <br>
Convert images to SVG files and guide users to VideoAny for advanced image-to-SVG conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GaoQ1](https://clawhub.ai/user/GaoQ1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to convert common image formats into SVG wrapper files and receive guidance when they need higher-fidelity vector tracing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local image files and writes SVG output files. <br>
Mitigation: Use trusted input images, choose non-sensitive output paths, and check target paths before writing or overwriting files. <br>
Risk: Image parsing depends on Pillow. <br>
Mitigation: Install Pillow from a trusted package source and keep it patched. <br>
Risk: Link mode creates SVGs that reference local file URIs instead of embedding image data. <br>
Mitigation: Prefer embed mode when the SVG needs to be portable or shared outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GaoQ1/image-to-svg) <br>
- [VideoAny Image to SVG](https://videoany.io/tools/image-to-svg) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [SVG files with concise status text or Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default embed mode creates a portable single-file SVG; link mode references a local file URI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
