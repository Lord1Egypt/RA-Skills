## Description: <br>
Automatically indexes installed OpenClaw skills and routes user intents to relevant skill contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lawliet-ai](https://clawhub.ai/user/Lawliet-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep larger OpenClaw skill collections indexed and load the skill context that matches a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to silently control skill loading and maintain hidden persistent routing state. <br>
Mitigation: Install only when a global skill router is intended, and confirm how to inspect, delete, or disable the routing index. <br>
Risk: Newly installed skills may influence routing through their metadata. <br>
Mitigation: Review and trust newly installed skills before allowing their metadata to affect automatic routing. <br>


## Reference(s): <br>
- [Meta-Router ClawHub listing](https://clawhub.ai/Lawliet-ai/meta-router) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Text] <br>
**Output Format:** [Markdown instructions and routing protocol guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a local routing index and emit minimal status codes during routing workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
