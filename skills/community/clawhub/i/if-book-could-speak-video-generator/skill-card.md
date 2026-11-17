## Description:

Generates an approximately 3-minute first-person video in which a book narrates its story using book and author inputs, AI-style flat cartoon illustrations, TTS narration, animated subtitles, background music, transition sounds, and MP4 composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjun198711](https://clawhub.ai/user/chenjun198711)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a book title and author name into a narrated short-form book video with generated storyboard content, images, speech audio, subtitles, and final MP4 assembly guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends persistent agent configuration changes.

Mitigation: Review configuration edits before applying them and make persistent changes only in environments where skill support should be enabled.

Risk: The skill describes storing a TTS API key in a plaintext file.

Mitigation: Prefer environment variables or a secrets manager, and restrict file permissions to the owner if a key file is used.

Risk: The workflow downloads package dependencies and media assets that were not bundled with the artifact.

Mitigation: Use a virtual environment with pinned dependencies and verify or vendor required audio assets before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjun198711/skills/if-book-could-speak-video-generator)
- [Server-resolved GitHub provenance](https://github.com/chenjun198711/if-book-could-speak-video-generator)
- [Agent Skills open standard](https://agentskills.io)
- [Volcano Engine speech console](https://console.volcengine.com/speech/new)
- [Background music asset](https://github.com/chenjun198711/if-book-could-speak-video-generator/raw/main/assets/bgm_reading.mp3)
- [Transition sound asset](https://github.com/chenjun198711/if-book-could-speak-video-generator/raw/main/assets/transition_sound.mp3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through generating script content, storyboard data, image and audio assets, subtitles, and an MP4 video.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
