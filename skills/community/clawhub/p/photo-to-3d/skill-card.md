## Description:

Converts a user-supplied photo into a clean isometric image with Gemini, then generates a .glb 3D model with the Tripo3D API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m15010495895-sudo](https://clawhub.ai/user/m15010495895-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and asset teams use this skill to turn 2D product, object, or reference images into generated 3D model assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to Gemini and Tripo3D for processing.

Mitigation: Avoid sensitive, private, or regulated images unless those services' policies and data handling meet your requirements.

Risk: The model download URL is returned by an external API.

Mitigation: Validate the returned model URL before fetching the generated asset.

Risk: Broad trigger phrases may invoke the workflow for requests that only loosely mention 3D generation.

Mitigation: Narrow triggers or confirm user intent before uploading images to third-party services.

## Reference(s):

- [Photo to 3D ClawHub Skill Page](https://clawhub.ai/m15010495895-sudo/skills/photo-to-3d)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [Tripo3D Platform](https://platform.tripo3d.ai/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG/GLB file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and TRIPO_API_KEY; writes an isometric PNG and final .glb model under the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
