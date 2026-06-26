## Description: <br>
Real-time voice conversations in Discord voice channels with Claude AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw or Clawdbot agent join Discord voice channels, transcribe spoken input, route it through the host agent, and speak generated responses back to participants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord voice audio may be listened to, transcribed, and sent to configured external STT or TTS providers. <br>
Mitigation: Disclose recording and transcription to channel participants, choose local providers for private conversations, and configure only providers that meet the deployment's data-handling requirements. <br>
Risk: Spoken input can reach the host agent and trigger its normal tool access. <br>
Mitigation: Restrict allowedUsers, review the host agent's tool permissions, and deploy with least-privilege credentials. <br>
Risk: Automatic channel joining can expose conversations unintentionally. <br>
Mitigation: Avoid autoJoinChannel unless needed and require explicit join commands for sensitive servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Discord voice interactions plus Markdown and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Discord bot token, ffmpeg, and optional STT/TTS provider credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
