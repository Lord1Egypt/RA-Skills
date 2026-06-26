## Description: <br>
Crop objects from images using bounding box annotations in COCO, YOLO, VOC, or LabelMe-style workflows, with optional padding and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and dataset maintainers use this skill to extract annotated objects from local image datasets for review, curation, or downstream computer-vision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated crop filenames can overwrite existing files in the selected output directory. <br>
Mitigation: Write outputs to a dedicated directory and review existing files before running batch crops. <br>
Risk: The script depends on Pillow for local image processing. <br>
Mitigation: Install Pillow from a trusted Python package source and keep the local environment maintained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/image-cropper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated image crop files when commands are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cropped image outputs or sprite-style image assets to a selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
