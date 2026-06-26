## Description: <br>
Computer vision and image processing using OpenCV WebAssembly for image processing, object detection, feature extraction, panorama stitching, photo filters, camera calibration, and machine learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run OpenCV-based image processing and computer vision operations through an OpenClaw WASM sandbox. It supports workflows such as enhancement, detection, feature matching, stitching, calibration, ML training and prediction, and batch conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a downloaded OpenCV WASM component. <br>
Mitigation: Install only when the WASM source is trusted and verify the downloaded component before use. <br>
Risk: Mapped folders may expose sensitive files or allow unintended overwrites. <br>
Mitigation: Map only a dedicated image working folder, avoid sensitive directories, and verify outputs before replacing originals. <br>


## Reference(s): <br>
- [OpenCV WASM Operations Reference](references/operations.md) <br>
- [OpenCV Skill on ClawHub](https://clawhub.ai/guyoung/opencv) <br>
- [OpenCV WASM Component Download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/opencv/files/opencv-component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown with inline command and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify image files in mapped sandbox directories depending on the requested OpenCV operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
