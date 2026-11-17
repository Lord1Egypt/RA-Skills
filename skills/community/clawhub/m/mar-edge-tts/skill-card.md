## Description:

mar-edge-tts generates text-to-speech audio from text using the SkillBoss API Hub TTS service with configurable voices, languages, rate, pitch, volume, and optional subtitle output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to turn requested text, summaries, or messages into spoken audio, including voice and prosody customization for accessibility, multitasking, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation is sent to the SkillBoss/HeyBoss TTS API.

Mitigation: Avoid converting secrets, private messages, regulated data, or confidential work unless the external provider and data-handling terms are acceptable.

Risk: Security evidence reports documentation mismatches around subtitle and dependency behavior.

Mitigation: Review the bundled scripts, package files, and subtitle behavior before installation or deployment.

Risk: Automatic TTS activation could speak unintended text when trigger handling is too broad.

Mitigation: Confirm the text to be converted before execution in sensitive or shared contexts.

Risk: Generated audio files may remain in the temporary edge-tts directory.

Mitigation: Clean up generated audio and subtitle files after delivery when they may contain sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-edge-tts)
- [Node Edge TTS guide](references/node_edge_tts_guide.md)
- [Voice testing page](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [MP3 audio files, MEDIA paths, JSON subtitle or configuration output, and Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and internet access; default audio files are written under a temporary edge-tts directory unless an output path is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
