## Description:

Oasis Audio Pro helps an agent generate personalized Chinese or English audio narration with background music through xplai.ai, optionally using local OpenClaw/QClaw context to shape the prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlelightsai](https://clawhub.ai/user/littlelightsai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to turn a request, notes, recent context, or longer material into a narrated audio piece. It selects an audio mode, voice, pacing, and personalization strategy, then submits the final composed prompt to xplai.ai and polls for the generated audio result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw/QClaw sessions, memory files, and USER.md to personalize audio, which can expose private local context to the prompt-building process.

Mitigation: Install and run it only when that local context access is acceptable; use non-personalized generation when context is unnecessary.

Risk: The final composed prompt is sent to xplai.ai and may indirectly contain sensitive themes derived from local context.

Mitigation: Review sensitive previews before using --allow-sensitive, and avoid sending prompts that contain personal, medical, financial, legal, credential, or account details.

Risk: Visitor JWT tokens and consent state are stored locally, and audit/debug modes can leave sensitive prompt or request details on disk or in logs.

Mitigation: Avoid --debug and --audit with sensitive content, and periodically review or delete ~/.oasis_audio, .oasis_audio_consent.json, and audit.log on shared machines.

## Reference(s):

- [Oasis Audio Pro ClawHub page](https://clawhub.ai/littlelightsai/skills/oasis-audio-pro)
- [Publisher profile](https://clawhub.ai/user/littlelightsai)
- [xplai.ai](https://www.xplai.ai/)
- [xplai.ai API endpoint](https://eagle-api.xplai.ai)
- [Audio Modes](artifact/audio_modes.md)
- [Text Architecture](artifact/text_architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated audio status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an audio generation request ID, status updates, and, on success, an xplai.ai audio URL; the generated media is MP3 audio with background music.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
