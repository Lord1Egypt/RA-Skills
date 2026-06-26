## Description: <br>
Image Annotation QC detects quality issues in bounding box and polygon segmentation annotations, supports COCO, YOLO, VOC, and LabelMe inputs, and generates local quality reports with optional visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data quality engineers use this skill to run local quality checks on image annotation datasets, identify labeling issues, and generate TXT, JSON, Excel, and visualization reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads selected local dataset folders and writes generated reports and visualizations to local paths. <br>
Mitigation: Run it only on intended dataset folders and use --output to keep generated reports separate from source annotations. <br>
Risk: The workflow depends on local Python packages such as Pillow and openpyxl. <br>
Mitigation: Install dependencies in a trusted Python environment before running the QC commands. <br>


## Reference(s): <br>
- [Annotation standards reference](references/standards.md) <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/image-annotation-qc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced tool writes local TXT, JSON, optional Excel, and PNG visualization report files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
