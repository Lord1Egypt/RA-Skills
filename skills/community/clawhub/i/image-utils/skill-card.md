## Description: <br>
Image Utils helps agents perform deterministic Pillow-based image operations such as resizing, cropping, compositing, format conversion, watermarking, image adjustments, and web optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to post-process generated or existing images, prepare web and social media variants, batch process image directories, and apply deterministic pixel-level transformations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download images from arbitrary URLs, including URLs that may be private, internal, or untrusted. <br>
Mitigation: Use trusted image URLs only and avoid private or internal URLs unless the network request is intended. <br>
Risk: The skill can save processed images to local file paths. <br>
Mitigation: Review output paths before execution and avoid writing sensitive images or overwriting important files. <br>
Risk: Optional Bria integration can send prompts or image-related data to an external API. <br>
Mitigation: Do not send confidential prompts or sensitive images to the Bria API unless that external processing is approved. <br>


## Reference(s): <br>
- [Image Utils code example](references/code-examples/image_utils.py) <br>
- [Image Utils on ClawHub](https://clawhub.ai/galbria/skills/image-utils) <br>
- [Bria AI skill](https://clawhub.ai/galbria/bria-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local image paths, remote image URLs, base64 image data, and optional Bria API credentials depending on the workflow.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact metadata reports 1.3.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
