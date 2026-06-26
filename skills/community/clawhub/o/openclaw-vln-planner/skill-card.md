## Description: <br>
Plans one high-level robot navigation step from a natural-language instruction, a current image, and optional historical images, returning a validated JSON action for a separate execution layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiktokdad](https://clawhub.ai/user/tiktokdad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to convert a navigation instruction plus visual observations into one bounded mid-level robot action for closed-loop replanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Robot camera frames and navigation context may be sent to an OpenAI-compatible multimodal gateway. <br>
Mitigation: Use only a trusted gateway, apply privacy controls for image data, and review data-handling requirements before deployment. <br>
Risk: Navigation predictions can be wrong or unsafe if connected directly to a physical robot. <br>
Mitigation: Keep dry_run enabled during testing, require human supervision, and use independent safety controls before real robot execution. <br>
Risk: Plaintext API keys or unpinned Python dependencies can increase operational exposure. <br>
Mitigation: Store API keys outside plaintext config where possible, and pin and audit Python dependencies before deployment. <br>


## Reference(s): <br>
- [Navigation Schema Reference](references/navigation-schema.md) <br>
- [OpenClaw VLN Planner ClawHub Page](https://clawhub.ai/tiktokdad/openclaw-vln-planner) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Code, Configuration] <br>
**Output Format:** [Pure JSON navigation action with supporting configuration and bridge guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Allowed actions are MOVE_FORWARD, TURN_LEFT, TURN_RIGHT, and STOP; invalid, uncertain, or unsafe results fall back to STOP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
