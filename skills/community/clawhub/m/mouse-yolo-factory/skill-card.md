## Description:

Generate simulated scratch defects, run YOLO model inference with auto-labeling, and merge mouse product defect image datasets with version control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwysbd](https://clawhub.ai/user/dwysbd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computer-vision engineers use this skill to create synthetic scratch examples, run YOLO-based defect inference on mouse product images, export labels, and roll labeled data into versioned training datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scratch generation can remove the images subfolder under the selected base_path.

Mitigation: Run the workflow only against copied datasets and verify base_path before execution.

Risk: YOLO inference can persist filenames and detection results to D:/aiagent/rag_database/detection_logs.jsonl.

Mitigation: Clear, relocate, or restrict access to the log when filenames or defect detections are sensitive.

Risk: Generated scratches and auto-labels may be inaccurate for production model training without review.

Mitigation: Inspect generated images, YOLO labels, and merged dataset versions before using them for training or evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwysbd/skills/mouse-yolo-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python workflow references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced workflows can create image files, YOLO label files, JSON/JSONL records, annotated preview images, and versioned dataset folders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
