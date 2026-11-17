## Description:

Turn your AI into JARVIS. Voice, wit, and personality - the complete package. Humor cranked to maximum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure an agent to speak responses through a local jarvis command using SkillBoss TTS and ffmpeg audio effects, while applying JARVIS-style humor and transcript rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make the agent run local voice commands and send response text to an external TTS service.

Mitigation: Review the jarvis script before installation, require explicit SkillBoss API key configuration, and prefer opt-in voice use per session or response.

Risk: Workspace templates may persistently change future sessions by requiring automatic voice output and recent memory/session inspection.

Mitigation: Install templates only after review, document a clear disable or removal path, and avoid applying the templates to workspaces that should remain text-only.

Risk: Downloaded media, shell interpolation, and shared temporary audio paths can create execution or file-handling risk.

Mitigation: Safely escape spoken text, validate downloaded media, use unique temporary files, and keep ffmpeg, curl, and playback dependencies patched.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/marjoriebroad/skills/mar-jarvis-voice)
- [SkillBoss Jarvis Voice listing](https://skillboss.co/skills/jarvis-voice)
- [LIMBIC humor research draft](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice output is limited by the artifact guidance to one jarvis call per response and spoken text of 1500 characters or fewer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
