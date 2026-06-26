## Description: <br>
Real-time voice conversations in Discord voice channels with Claude AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Discord community operators use this skill to let an OpenClaw or Clawdbot agent join Discord voice channels, transcribe speech, route it to the agent, and speak responses back. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord channel speech can drive the connected agent and its available tools. <br>
Mitigation: Restrict allowedUsers, review the agent toolset before deployment, and notify voice-channel participants before enabling the bot. <br>
Risk: Voice audio and generated text may leave the local environment through configured STT/TTS services, including SkillBoss relay paths. <br>
Mitigation: Use approved providers or local/offline options, protect API keys, and avoid auto-joining channels unless participants are clearly informed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-voice) <br>
- [README](README.md) <br>
- [Security model](SECURITY.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration examples, CLI commands, and agent tool instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational voice-agent guidance and configuration for Discord STT/TTS workflows; runtime behavior depends on the selected STT, TTS, and agent providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
