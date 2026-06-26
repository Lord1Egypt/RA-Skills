## Description: <br>
Generates stylized character portraits from an authorized image URL and prompt using Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to check Media.io credits, submit a character-generation task from an authorized image URL and prompt, poll for completion, and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and image URLs to Media.io and may use account credits. <br>
Mitigation: Use user-owned or authorized image URLs, avoid private or internal images unless they are safe to share with Media.io, check credits before generation, and monitor Media.io usage. <br>
Risk: The skill depends on MEDIAIO_API_KEY for external API calls. <br>
Mitigation: Store the key in the environment, avoid logging or returning raw API keys, and stop with a clear message on authentication or credit errors. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>
- [ClawHub release page](https://clawhub.ai/wondershare-boop/mediaio-ai-character-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and cURL examples; returns generated image URLs or clear status and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and a Media.io-reachable authorized image URL; generation is asynchronous and may consume Media.io credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
