## Description:

MiniMax Speech helps agents use MiniMax APIs for synchronous and asynchronous text-to-speech, voice cloning, voice design, voice lookup, and voice deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silingyuan0](https://clawhub.ai/user/silingyuan0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate MiniMax speech synthesis workflows, including producing local audio files and managing custom voices through the MiniMax API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text prompts and reference voice samples are sent to MiniMax APIs.

Mitigation: Avoid submitting private or sensitive content unless the user has approved that disclosure and the MiniMax account terms allow it.

Risk: Voice cloning can create or manage custom voice identities.

Mitigation: Clone voices only from samples collected with proper consent and keep generated voice identifiers controlled.

Risk: The skill can delete remote voice records by voice_id.

Mitigation: Confirm the intended voice_id before deletion and avoid automating deletion without a review step.

Risk: Generated audio is written to a caller-provided local path.

Mitigation: Use explicit output paths in controlled directories to avoid overwriting unintended files.

## Reference(s):

- [MiniMax Speech API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/silingyuan0/skills/minimax-speech-generate)
- [ClawHub publisher profile](https://clawhub.ai/user/silingyuan0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python function calls, shell commands, JSON configuration examples, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mp3, wav, or pcm audio files and MiniMax task or voice identifiers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
