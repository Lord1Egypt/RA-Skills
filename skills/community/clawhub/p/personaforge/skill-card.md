## Description: <br>
Persona Forge is an AI companion skill that generates personality-based characters from chat logs, images, or descriptions, remembers user traits, and lets relationships evolve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgt9721](https://clawhub.ai/user/wgt9721) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create and interact with configurable AI companion characters. It can analyze user-provided character names, descriptions, chat logs, images, and notes to produce character profiles, maintain relationship memory, schedule proactive messages, and support optional image, TTS, STT, web search, and messaging-channel integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create persistent local relationship and memory files. <br>
Mitigation: Review stored state regularly and delete the state directory when the companion or its retained memory is no longer desired. <br>
Risk: The skill may create recurring scheduled messages. <br>
Mitigation: Review, disable, or remove cron jobs before deployment unless proactive companion messages are intended. <br>
Risk: Uploaded chat logs may include other people's conversations or sensitive details. <br>
Mitigation: Only upload logs with appropriate consent and avoid including sensitive third-party content. <br>
Risk: Optional message channels, web search, image generation, TTS, and STT providers can expand data exposure. <br>
Mitigation: Enable only the integrations needed for the deployment and review provider settings before use. <br>


## Reference(s): <br>
- [Persona Forge ClawHub page](https://clawhub.ai/wgt9721/personaforge) <br>
- [Character profile template](references/character-profile-template.md) <br>
- [Setup guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated character profiles, JSON state examples, setup instructions, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state files, relationship memory, cron-based proactive messages, and integration guidance for messaging channels, web search, image generation, TTS, and STT.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
