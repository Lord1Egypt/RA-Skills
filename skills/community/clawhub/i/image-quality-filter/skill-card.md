## Description: <br>
Detects low-quality images by analyzing blur, brightness, and resolution so image datasets can be cleaned efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and dataset curators use this skill to find blurry, dark, over-bright, or low-resolution images before keeping, moving, or deleting them from local image folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move or delete local image files after images are flagged as low quality. <br>
Mitigation: Use the default list action first, review flagged images and threshold settings, prefer move over delete for important datasets, and keep backups before deletion. <br>
Risk: Quality thresholds can flag acceptable images as low quality. <br>
Mitigation: Tune blur, brightness, and resolution thresholds for the dataset and manually review results before taking destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/image-quality-filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with command examples and local file-operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May list matching image paths and quality scores, or move/delete flagged local files when the user chooses those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
