## Description: <br>
Runs Media.io's asynchronous female gender-swap image effect from a user-provided image URL and returns generated preview URLs after polling for task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Media.io credits, submit an authorized portrait image URL for a female gender-swap generation task, poll task status, and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public description may lead users to expect a Studio Ghibli-style filter even though the artifact implements a Media.io female gender-swap workflow. <br>
Mitigation: Present the skill as a gender-swap workflow before use and do not describe generated results as Ghibli-style output. <br>
Risk: The workflow sends image URLs to Media.io and may consume paid credits. <br>
Mitigation: Use a dedicated revocable Media.io API key, check credits before generation, and submit only images the user owns or is authorized to process. <br>
Risk: Generated results are synthetic edits of people and could be mistaken for identity or biometric assertions. <br>
Mitigation: Label outputs as edited synthetic media and avoid claims about identity verification or biometric certainty. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-ai-gender-swap) <br>
- [Media.io platform documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY, curl, an externally reachable PNG/JPEG/JPG image URL, and asynchronous polling by task_id.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
