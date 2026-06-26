## Description: <br>
Uses Jiekou AI to run multimodal tasks including text-to-image, image editing, text-to-video, image-to-video, text-to-speech, speech-to-text, and multimodal understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ximasadila](https://clawhub.ai/user/ximasadila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Jiekou's cloud API for media generation, media editing, speech conversion, transcription, and basic multimodal analysis from chat-driven requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, audio, images, and video references may be sent to Jiekou's cloud API. <br>
Mitigation: Use the skill only for media and prompts approved for external processing, and review Jiekou privacy and pricing terms before submitting sensitive or paid tasks. <br>
Risk: The skill documentation permits API keys in chat messages and local config files. <br>
Mitigation: Do not paste API keys into chat; use a protected secret or environment variable with a dedicated low-privilege key and restrict permissions on any local config file. <br>
Risk: Generation and transcription requests can consume paid API quota. <br>
Mitigation: Confirm the intended task, model, and expected cost before execution, and use account-level limits where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ximasadila/jiekou-multimodal) <br>
- [API reference](artifact/references/api-reference.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Test cases](artifact/references/test-cases.md) <br>
- [Jiekou API base URL](https://api.jiekou.ai) <br>
- [Jiekou API key management](https://jiekou.ai/settings/key-management) <br>
- [Jiekou pricing](https://jiekou.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, JSON request examples, API result URLs, and progress updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated image, video, or audio URLs and may poll asynchronous video tasks until completion.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
