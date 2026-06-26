## Description: <br>
Generate AI images via ImaginePro API (Midjourney, Flux, Nano Banana, Lumi Girl, video). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamzifei](https://clawhub.ai/user/iamzifei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to call ImaginePro for image and video generation, prompt enhancement, upscaling, background removal, and status polling from shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, image URLs, and optional webhook endpoints to ImaginePro for processing. <br>
Mitigation: Avoid confidential prompts, private or internal image URLs, personal data, and sensitive webhook endpoints unless ImaginePro processing is acceptable. <br>
Risk: The skill uses an ImaginePro account API key and can spend account credits. <br>
Mitigation: Use a dedicated API key where possible, monitor credit usage, and check available credits before large batches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamzifei/imaginepro-api) <br>
- [ImaginePro AI agent skill documentation](https://platform.imaginepro.ai/ai-agent-skill) <br>
- [ImaginePro API key setup](https://platform.imaginepro.ai/dashboard/setup) <br>
- [ImaginePro pricing](https://platform.imaginepro.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMAGINEPRO_API_KEY and may return message IDs, generation status, image URLs, video task results, or error JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
