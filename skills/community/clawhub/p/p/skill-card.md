## Description: <br>
P图 provides image loading, saving, resizing, cropping, format conversion, enhancement, filters, stitching, basic background removal, and text overlay utilities for creative image editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to script common image editing workflows, including transformations, filters, image composition, background cleanup, and text placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image files from untrusted sources may exercise vulnerabilities in the image-processing dependency. <br>
Mitigation: Use a reviewed, pinned Pillow version, keep it updated, and process untrusted images in a constrained environment. <br>
Risk: The dependency declaration allows newer Pillow releases through an unpinned lower bound. <br>
Mitigation: Pin Pillow to an approved version in deployment environments and update deliberately after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/p) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance] <br>
**Output Format:** [Python image objects and image files with Markdown or code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Pillow for local image processing; output files depend on caller-provided paths and image formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md, README.md, src/p_skill/__init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
