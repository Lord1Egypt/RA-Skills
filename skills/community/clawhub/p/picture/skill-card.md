## Description: <br>
Picture is a local Python image-processing skill for loading, saving, resizing, cropping, format conversion, enhancement, filters, image stitching, background removal, and text overlays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local image editing workflows to Python-based agents, including common transformations, visual enhancements, composition, simple background removal, and text annotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing untrusted or oversized images can expose the runtime to Pillow parser issues or resource exhaustion. <br>
Mitigation: Use a reviewed, current Pillow version, keep dependency scanning enabled, and avoid untrusted oversized inputs. <br>
Risk: Saving edited outputs over source filenames can overwrite original images. <br>
Mitigation: Write outputs to new filenames or a separate output directory before replacing originals. <br>
Risk: Threshold-based background removal can remove foreground pixels when colors are similar. <br>
Mitigation: Preview edited images and adjust threshold, target color, tolerance, or smoothing values before using results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/picture) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python API calls; processed image files when the code is executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local images through Pillow and writes outputs to caller-selected file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md, README.md, package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
