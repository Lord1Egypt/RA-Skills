## Description:

Image Annotation QC detects quality issues in bounding box and polygon segmentation annotations and generates reports and visualizations for COCO, YOLO, VOC, and LabelMe datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and data quality teams use this skill to inspect image annotation datasets, detect bounding-box and polygon quality issues, and generate QC reports for AI training data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted annotation files can make the tool read images outside the selected image folder.

Mitigation: Run the skill in a dedicated project directory or sandbox, and keep visualization disabled for untrusted datasets until image-path containment is fixed.

Risk: Generated Excel reports can contain unsafe values from untrusted labels.

Mitigation: Avoid opening generated XLSX files from untrusted annotation sources; prefer TXT or JSON reports when reviewing untrusted datasets.

Risk: Unpinned Python dependencies can introduce environment drift or unexpected package changes.

Mitigation: Install Pillow and openpyxl in an isolated Python environment with reviewed, pinned versions.

## Reference(s):

- [Image Annotation QC ClawHub listing](https://clawhub.ai/mingo-318/skills/image-annotation-qc)
- [Image annotation standards reference](references/standards.md)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, guidance]

**Output Format:** [Markdown guidance with bash and Python examples; generated QC artifacts may include TXT, JSON, XLSX, and PNG visualization files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional report and visualization features use Pillow and openpyxl.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
