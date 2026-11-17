## Description:

Portrait Compare helps an agent compare two uploaded face photos, calculate a similarity score, and report a same-person likelihood with caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavierjiezou](https://clawhub.ai/user/xavierjiezou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to compare two user-provided face images for similarity in workflows such as photo comparison or identity-check assistance. Results should be treated as decision support, not definitive identity proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive face images and may be triggered broadly for identity-style comparisons.

Mitigation: Use it only when the people in the photos are authorized for comparison and prefer explicit user confirmation before each comparison.

Risk: Face similarity scores can be affected by photo quality, lighting, angle, expression, age gap, makeup, glasses, and detector limitations.

Mitigation: Present results as decision support with uncertainty language and recommend human review for borderline or high-impact outcomes.

Risk: The script can write annotated comparison images to temporary or user-specified paths.

Mitigation: Delete generated output images when no longer needed and avoid retaining sensitive face data longer than necessary.

Risk: Optional ONNX models may be loaded from /tmp or the current directory if present.

Mitigation: Use pinned, checksum-verified model files from a trusted location instead of unverified local files.

## Reference(s):

- [Face Recognition Algorithm Notes](references/algorithm_notes.md)
- [OpenCV YuNet face detection model](https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx)
- [OpenCV SFace face recognition model](https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx)
- [ClawHub skill page](https://clawhub.ai/xavierjiezou/skills/portrait-compare)
- [Publisher profile](https://clawhub.ai/user/xavierjiezou)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown summary with similarity score, same-person likelihood, method details, caveats, and optional annotated image file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an annotated comparison image when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
