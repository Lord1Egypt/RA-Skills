## Description:

Use GLM-4.7V's multimodal grounding capability to detect and locate objects, text, UI elements, and regions in images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qijimrc](https://clawhub.ai/user/qijimrc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ground requested objects, text, UI elements, or image regions by calling a configured multimodal model endpoint, parsing bounding boxes, and producing annotated visual results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image contents and prompts are sent to an internal HTTP model endpoint with proxy bypass configured.

Mitigation: Use only trusted endpoints and confirm transport security, logging, retention, and proxy policy before sending sensitive images.

Risk: Annotated output images may persist on disk after visualization.

Mitigation: Choose known save paths and remove generated files when they contain sensitive content.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Files]

**Output Format:** [Markdown guidance with Python code snippets and saved annotated image output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounding boxes are normalized to 0-1000 coordinates and can be converted to pixel coordinates for visualization.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
