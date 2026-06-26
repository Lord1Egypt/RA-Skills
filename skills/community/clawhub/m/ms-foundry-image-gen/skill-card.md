## Description: <br>
Azure Foundry image generation skill for OpenClaw; generates images via a Foundry deployment and returns image bytes or URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacqueskang](https://clawhub.ai/user/jacqueskang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate images through their configured Azure Foundry images deployment and retrieve either image bytes or response URLs. It is useful when an agent needs shell-oriented guidance for calling a Foundry image-generation endpoint with user-provided credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image-generation requests are sent to the configured Azure Foundry endpoint. <br>
Mitigation: Install only when Azure Foundry processing is intended, and use a trusted HTTPS endpoint controlled by the user or organization. <br>
Risk: The Foundry API key is the primary credential for the deployment. <br>
Mitigation: Keep FOUNDRY_API_KEY private, scope it appropriately, and avoid exposing it in command history, logs, or shared files. <br>
Risk: Image-generation calls can create usage charges or quota consumption. <br>
Mitigation: Monitor Azure Foundry usage and costs for the configured deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacqueskang/ms-foundry-image-gen) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to call an Azure Foundry images deployment and save response JSON and decoded image output under /tmp when the deployment returns base64 image data.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
