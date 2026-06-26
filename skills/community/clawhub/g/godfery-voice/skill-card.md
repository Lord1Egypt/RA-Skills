## Description: <br>
Enables real-time Discord voice conversations by transcribing speech, routing it through an agent, and playing synthesized responses back into the channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Discord bot operators use this skill to add live voice interaction to OpenClaw or Clawdbot deployments, including voice-channel join and leave controls, speech transcription, agent response generation, and text-to-speech playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord speech and generated text can be recorded, transcribed, sent to external services, processed by the agent, and spoken back in the channel. <br>
Mitigation: Use the skill only in Discord channels where participants understand this processing, and choose local or offline providers when speech data should not leave the host. <br>
Risk: Provider labels can understate that SkillBoss or HeyBoss may process data for hosted speech services. <br>
Mitigation: Treat SkillBoss and HeyBoss as data processors when configuring hosted STT or TTS providers and review credential and data-handling requirements before deployment. <br>
Risk: An empty allowedUsers configuration allows all users in joined channels to interact with the bot and trigger provider calls. <br>
Mitigation: Set allowedUsers to the intended Discord user IDs and avoid autoJoin unless automatic channel entry is explicitly required. <br>
Risk: The skill depends on the OpenClaw host, native audio dependencies, and networked speech providers for real-time operation. <br>
Mitigation: Run it on a patched OpenClaw host with current dependencies, valid Discord voice permissions, and monitored provider credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/godferylindsay/godfery-voice) <br>
- [Publisher profile](https://clawhub.ai/user/godferylindsay) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [Security model](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, configuration, command, and operational guidance for a Discord voice agent skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
