## Description: <br>
Use GLM-4.7V multimodal grounding to detect and locate requested objects, text, UI elements, or image regions and produce bounding-box guidance and visualized outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qijimrc](https://clawhub.ai/user/qijimrc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an agent through image-grounding workflows: call a configured GLM-4.7V endpoint, parse normalized bounding boxes, and save an annotated output image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends user-provided images to a configured GLM model endpoint. <br>
Mitigation: Install only if the endpoint is trusted for the images being processed, and avoid sending confidential images unless the endpoint's privacy and retention practices are acceptable. <br>
Risk: The workflow requires NO_PROXY configuration for model-host access. <br>
Mitigation: Keep NO_PROXY limited to the model host and review local helper modules before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce saved annotated image files from user-provided images and model-returned bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
