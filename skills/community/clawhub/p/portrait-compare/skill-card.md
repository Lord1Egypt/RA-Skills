## Description: <br>
Compares two face photos, detects the largest visible face in each image, calculates a similarity score, and reports whether the photos likely show the same person. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xavierjiezou](https://clawhub.ai/user/xavierjiezou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to compare two authorized face photos for similarity, identity-check assistance, photo matching, or human review triage. Results should be treated as advisory and not as the sole basis for important identity decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face photos and generated comparison images may contain sensitive biometric data. <br>
Mitigation: Process only images the user is authorized to compare and delete generated result images such as /tmp/face_result.jpg when finished. <br>
Risk: Similarity scores can be affected by image quality, lighting, angle, occlusion, age differences, or the selected algorithm mode. <br>
Mitigation: Present results as advisory, include uncertainty when appropriate, and require human review for important identity decisions. <br>
Risk: Optional ONNX model files used for high-precision mode are loaded from local paths if present. <br>
Mitigation: Verify optional model files before use and rely on the bundled general-purpose OpenCV path when model provenance is uncertain. <br>


## Reference(s): <br>
- [Algorithm Notes](references/algorithm_notes.md) <br>
- [YuNet ONNX model](https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx) <br>
- [SFace ONNX model](https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx) <br>
- [ClawHub skill page](https://clawhub.ai/xavierjiezou/portrait-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and a generated local result image path when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a similarity score, a same-person judgment, the algorithm used, detected face boxes, and optionally an annotated comparison image.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
