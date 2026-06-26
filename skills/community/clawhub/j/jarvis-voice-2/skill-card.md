## Description: <br>
Adds JARVIS-style voice output, visible transcripts, and humor guidance to an OpenClaw agent using SkillBoss TTS and local audio playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to make agent replies trigger a local Jarvis voice command, send spoken text to SkillBoss TTS, apply audio effects, play audio locally, and show a matching transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each spoken reply can send text to SkillBoss cloud TTS. <br>
Mitigation: Avoid speaking sensitive content, protect SKILLBOSS_API_KEY, and review SkillBoss data handling before deployment. <br>
Risk: Routine replies can execute a local jarvis command and play audio automatically. <br>
Mitigation: Review and pin the exact jarvis script before placing it in PATH, and install only where automatic local audio playback is intended. <br>
Risk: Workspace templates can persist voice, humor, memory-read, and daily-log behavior across sessions. <br>
Mitigation: Copy the VOICE, SESSION, and HUMOR templates only for workspaces where persistent Jarvis behavior is desired. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/marjoriebroad/jarvis-voice-2) <br>
- [SkillBoss Jarvis Voice Page](https://skillboss.co/skills/jarvis-voice) <br>
- [LIMBIC Humor Research Draft](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md) <br>
- [TinkerClaw Project](https://github.com/globalcaos/tinkerclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcript with a background shell command for local audio playback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spoken output uses the local jarvis command, SkillBoss TTS, ffmpeg audio effects, and a visible Jarvis transcript.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
