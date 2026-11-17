## Description:

Computer vision and image processing using OpenCV WebAssembly for image processing, object detection, feature extraction, panorama stitching, photo filters, camera calibration, and machine learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run OpenCV-based image processing, detection, feature, stitching, photo, calibration, machine learning, and batch workflows through a WebAssembly sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs a mutable, unverified WebAssembly binary from an external GitHub branch.

Mitigation: Install only if the publisher and remote source are trusted, and prefer a pinned release or verified SHA-256 for the WASM file.

Risk: Sandbox directory mappings can expose local files to image-processing operations.

Mitigation: Map only the specific image directory needed for each run and use separate output folders to avoid overwriting originals.

Risk: Network access during execution can increase exposure if the component or workflow is compromised.

Mitigation: Keep network access disabled unless it is strictly required for the task.

## Reference(s):

- [OpenCV WASM Operations Reference](references/operations.md)
- [OpenCV ClawHub Skill Page](https://clawhub.ai/guyoung/skills/opencv)
- [OpenCV WASM Component Download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/opencv/files/opencv-component.wasm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operation-specific guidance for invoking a WebAssembly sandbox against user-provided image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
