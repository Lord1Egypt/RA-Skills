## Description: <br>
Local OPUS/Ogg voice-reply pipeline for Feishu/Discord with structured voice customization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenured-master-chef-607](https://clawhub.ai/user/tenured-master-chef-607) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local text-to-speech voice reply workflow that generates Ogg/Opus audio and prepares voice responses for Feishu or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an unauthenticated local text-to-speech API. <br>
Mitigation: Keep the server bound to 127.0.0.1 and do not expose the port on shared or public networks. <br>
Risk: Uploaded voice samples and generated audio are stored on disk. <br>
Mitigation: Upload only voices you have permission to use, choose a narrow output directory, and periodically delete old voice, cache, and output files. <br>
Risk: Generated audio can be sent to Feishu or Discord destinations. <br>
Mitigation: Verify the intended destination before sending generated audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenured-master-chef-607/local-voice-reply) <br>
- [Voice Server v3 documentation](server/VOICE_SERVER_V3.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API call parameters, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides generation of local Ogg/Opus voice reply files and delivery through Feishu or Discord.] <br>

## Skill Version(s): <br>
3.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
