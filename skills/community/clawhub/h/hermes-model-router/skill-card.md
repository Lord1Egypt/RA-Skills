## Description: <br>
Automatically routes tasks to local or cloud AI models based on task complexity while preserving context continuity and single-entry model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to classify a requested task and choose a local or cloud model provider at task start, reducing cost for simple work and reserving provider models for complex or iterative work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex-task prompts may be routed to cloud model providers. <br>
Mitigation: Treat provider-routed prompts as potentially leaving the local machine and avoid sending sensitive data unless the provider handling model is acceptable. <br>
Risk: Provider configuration may include sensitive values in a plain local config file. <br>
Mitigation: Avoid placing API keys or sensitive secrets in the config file unless that storage model is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freepengyang/hermes-model-router) <br>
- [Publisher profile](https://clawhub.ai/user/freepengyang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with inline shell commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task classifications include complexity, routing recommendation, and rationale; verbose mode can include selected local or cloud model names and matched keywords.] <br>

## Skill Version(s): <br>
v1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
