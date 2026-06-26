## Description: <br>
Turn your AI into JARVIS. Voice, wit, and personality -- the complete package. Humor cranked to maximum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make an OpenClaw agent produce JARVIS-style spoken replies, visible Markdown transcripts, and witty conversational behavior through local audio tooling and SkillBoss text-to-speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends spoken reply text to the external SkillBoss text-to-speech service. <br>
Mitigation: Use it only where that text sharing is acceptable, protect SKILLBOSS_API_KEY, and avoid private, shared, or compliance-sensitive workspaces unless additional confirmation or mute controls are added. <br>
Risk: The skill automatically runs a local jarvis command for audio playback. <br>
Mitigation: Review the jarvis executable on PATH before enabling the skill and confirm that ffmpeg, aplay, curl, and audio playback behavior match the workspace policy. <br>
Risk: The provided templates can persistently change future OpenClaw sessions by auto-loading voice and humor instructions. <br>
Mitigation: Install the templates only when persistent voice behavior is desired, and remove or disable them for workspaces that should not auto-run voice output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/mar-jarvis-voice) <br>
- [SkillBoss Jarvis Voice Page](https://skillboss.co/skills/jarvis-voice) <br>
- [LIMBIC Humor Research Draft](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md) <br>
- [TinkerClaw Project](https://github.com/globalcaos/tinkerclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown transcripts with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spoken text is constrained by the skill to short English voice output, with one background jarvis command per response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
