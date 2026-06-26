## Description: <br>
Intelligently recommends optimal AI models based on task requirements by reading the user's OpenCLAW configuration and providing context-aware model suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garygou1024](https://clawhub.ai/user/garygou1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose an appropriate AI model from the models already configured in their local OpenCLAW setup for tasks such as coding, image analysis, reasoning, long-document work, and fast responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenCLAW configuration to identify available model IDs, and that configuration may contain endpoints, provider details, tokens, or other sensitive settings. <br>
Mitigation: Use the skill for model selection without asking it to print or share the full configuration, and review any output before copying configuration details elsewhere. <br>


## Reference(s): <br>
- [Model Capability Reference](references/comparison.md) <br>
- [ClawHub skill page](https://clawhub.ai/garygou1024/local-config-model-recommender) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown recommendations with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are scoped to models available in the user's local OpenCLAW configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
