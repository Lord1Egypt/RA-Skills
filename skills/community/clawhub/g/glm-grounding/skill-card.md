## Description: <br>
Use GLM-4.7V's multimodal grounding capability to detect and locate objects/text in images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qijimrc](https://clawhub.ai/user/qijimrc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to call a GLM-4.7V multimodal endpoint, parse normalized bounding boxes from its text response, and visualize object or text locations in supplied images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are sent to the configured GLM endpoint for grounding. <br>
Mitigation: Use a trusted endpoint and avoid sensitive images unless its logging, retention, and access controls are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qijimrc/glm-grounding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and concise workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe generated bounding boxes and annotated image outputs when used with caller-provided utilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
