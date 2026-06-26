## Description: <br>
Generates simulated scratch defects, runs YOLO model inference with auto-labeling, and merges mouse product defect image datasets with versioned outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dwysbd](https://clawhub.ai/user/Dwysbd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computer-vision engineers use this skill to create synthetic scratch examples, pre-label mouse product images with a YOLO model, and merge new annotations into versioned YOLO datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed persistent logging and unsafe local path behavior. <br>
Mitigation: Review and edit all paths before installation, run packaged scripts by relative path, and disable or redirect the detection log when image-derived metadata should not be retained. <br>
Risk: The workflows operate on image datasets and can overwrite, copy, merge, or regenerate local dataset files. <br>
Mitigation: Back up datasets before generation or merging and test on a small copy before using production data. <br>
Risk: Model-based auto-labeling can create incorrect annotations if the YOLO model or confidence threshold is unsuitable. <br>
Mitigation: Use only trusted YOLO model files and review generated labels before adding them to a training dataset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dwysbd/mouse-yolo-factory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown guidance with command-line examples and Python workflow descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for local scripts that create images, YOLO label files, JSONL detection logs, visualized detections, merged datasets, and dataset logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
