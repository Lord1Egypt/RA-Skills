## Description: <br>
Uses PPIO to perform multimodal tasks including text-to-image, image-to-image, text-to-video, image-to-video, text-to-speech, and speech-to-text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ximasadila](https://clawhub.ai/user/ximasadila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images, edit images, create videos, generate speech, and transcribe audio through PPIO APIs. It provides configuration guidance, progress messages, endpoint examples, and handling for asynchronous media tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses paid PPIO API calls and handles API keys. <br>
Mitigation: Use a restricted PPIO key stored outside conversation history, protect ~/.ppio/config.json with appropriate file permissions, and review expected costs before running generation tasks. <br>
Risk: Prompts, images, audio, and generated task metadata are sent to PPIO for processing. <br>
Mitigation: Avoid submitting private photos, meeting recordings, confidential business text, personal data, or regulated content unless PPIO processing is approved for that data. <br>
Risk: The skill documentation allows API keys to be supplied directly in user messages. <br>
Mitigation: Prefer configuration through ~/.ppio/config.json or PPIO_API_KEY and do not paste real API keys into chat transcripts. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ximasadila/ppio-multimodal) <br>
- [PPIO API key management](https://ppio.com/settings/key-management) <br>
- [PPIO models](https://ppio.com/models) <br>
- [PPIO pricing](https://ppio.com/pricing) <br>
- [PPIO console](https://ppio.com/console) <br>
- [PPIO documentation](https://docs.ppio.com) <br>
- [API reference](references/api-reference.md) <br>
- [Task examples](references/examples.md) <br>
- [Test cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, curl examples, status messages, task IDs, generated media URLs, and transcription text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PPIO API key and may return PPIO-hosted media URLs, asynchronous task status, cost estimates, actual spend, or API error guidance.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
