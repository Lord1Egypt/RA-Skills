## Description: <br>
Placeholder skill for image-to-image workflows on skills.video. Use when the user is asking about i2i generation and the concrete API contract has not been implemented yet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills-video](https://clawhub.ai/user/skills-video) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this placeholder to respond transparently to image-to-image workflow requests on skills.video while the concrete API contract is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect the skill to generate or transform images even though image-to-image support is not implemented. <br>
Mitigation: State that i2i is currently a placeholder and confirm model-specific documentation or an OpenAPI contract before proceeding. <br>
Risk: Invented endpoint fields or upload semantics could lead to incorrect guidance. <br>
Mitigation: Do not guess image input formats, endpoint names, polling behavior, credentials, or network calls; require verified provider documentation before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skills-video/i2i) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; the skill directs the agent to avoid undocumented image-to-image API assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
