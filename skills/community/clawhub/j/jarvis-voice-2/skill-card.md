## Description:

Turn your AI into JARVIS with voice, wit, and personality, with humor set to maximum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add command-backed voice output, visible Jarvis-prefixed markdown transcripts, and a high-frequency humor/personality layer to agent replies. It is intended for Linux environments configured with SkillBoss API access and local audio tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes future agent behavior through workspace templates and can force always-speak behavior.

Mitigation: Review and edit the templates before copying them into a workspace, and avoid enabling always-speak or session-bootstrap rules in sensitive or shared environments.

Risk: Selected response text may be sent to SkillBoss for audio generation.

Mitigation: Avoid using voice output for sensitive content and confirm that users are comfortable with SkillBoss API processing before enabling the skill.

Risk: The skill relies on command-backed audio output through a local jarvis script and external tools.

Mitigation: Inspect the jarvis script and required binaries before use, keep the API key scoped appropriately, and run the command only in trusted local environments.

Risk: Startup greetings can use recent memory or session context.

Mitigation: Disable or narrow the session bootstrap behavior where recent memory may expose private or irrelevant context.

## Reference(s):

- [ClawHub Jarvis Voice skill page](https://clawhub.ai/marjoriebroad/skills/jarvis-voice-2)
- [SkillBoss Jarvis Voice information](https://skillboss.co/skills/jarvis-voice)
- [LIMBIC computational humor reference](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md)
- [TinkerClaw project reference](https://github.com/globalcaos/tinkerclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with a visible transcript, shell-command execution guidance, and workspace template configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice output uses a local jarvis command, SkillBoss TTS, ffmpeg audio effects, and aplay playback when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
