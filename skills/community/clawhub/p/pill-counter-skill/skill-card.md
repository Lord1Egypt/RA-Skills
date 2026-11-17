## Description:

Pill Counter Skill counts pills from images using local OpenCV or optional MiMo V2 Omni AI, classifies 13 pill shapes, and can produce text, JSON, CSV, and annotated-image outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonxuan](https://clawhub.ai/user/johnsonxuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to count and classify pills in image files, with a local OpenCV path for offline use and an optional AI path for more complex images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI mode can upload medication photos to Xiaomi MiMo.

Mitigation: Use the local OpenCV mode for sensitive medication photos unless external image processing is acceptable.

Risk: File handling is broader than the declared pill-counter workspace scope and output paths can overwrite files.

Mitigation: Run the skill only on files inside the declared pill-counter workspace and choose output paths that do not replace important files.

Risk: Pill counts can be inaccurate for overlapping or complex images.

Mitigation: Review the generated count, CSV report, and annotated image before using the result for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsonxuan/skills/pill-counter-skill)
- [Xiaomi MiMo chat completions API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, files]

**Output Format:** [Terminal text or JSON, with optional CSV report and annotated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts an image path, optional AI mode, optional JSON output, and optional CSV or annotated-image output paths.]

## Skill Version(s):

4.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
