## Description: <br>
Monet AI is an AI content generation API guide for agents covering video, image, and music generation workflows across supported models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seekton](https://clawhub.ai/user/seekton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create workflows that submit authenticated Monet AI generation jobs for video, image, and music outputs, poll task status, and retrieve generated asset URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Monet account API key to submit generation jobs. <br>
Mitigation: Store MONET_API_KEY in an environment variable, avoid hardcoding it, and set clear approval or budget expectations before use. <br>
Risk: Prompts and uploaded media are sent to monet.vision for generation. <br>
Mitigation: Do not upload private files, secrets, proprietary media, personal data, or sensitive prompts unless sharing them with monet.vision is acceptable. <br>


## Reference(s): <br>
- [Monet AI ClawHub listing](https://clawhub.ai/seekton/monet-ai) <br>
- [Publisher profile](https://clawhub.ai/user/seekton) <br>
- [Monet AI](https://monet.vision) <br>
- [Monet API keys](https://monet.vision/skills/keys) <br>
- [Create async task endpoint](https://monet.vision/api/v1/tasks/async) <br>
- [Create streaming task endpoint](https://monet.vision/api/v1/tasks/sync) <br>
- [Upload file endpoint](https://monet.vision/api/v1/files) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONET_API_KEY and sends prompts or media to monet.vision for generation.] <br>

## Skill Version(s): <br>
1.0.9 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
