## Description: <br>
Picture Edit helps agents perform local image loading, saving, resizing, cropping, format conversion, enhancement, filters, stitching, simple background removal, and text overlays through a Python image-processing package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to script common image-editing workflows, including resizing, cropping, enhancing, filtering, compositing, removing simple backgrounds, and placing text on images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing untrusted images can expose the runtime to dependency-level image parsing vulnerabilities. <br>
Mitigation: Run the skill in a virtual environment and pin Pillow to a current reviewed version before handling untrusted files. <br>
Risk: The skill reads and writes local image paths supplied by the user or agent workflow. <br>
Mitigation: Review input and output paths before execution and restrict runs to an intended working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/picture-edit) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files when the generated or executed workflow saves edited images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill metadata, and package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
