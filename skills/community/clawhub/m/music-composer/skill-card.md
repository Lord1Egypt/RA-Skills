## Description:

Music Composer plans music-generation prompts and mmx CLI commands for instrumental tracks, Chinese or English songs, and cover-style transformations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhouxinliang](https://clawhub.ai/user/yuhouxinliang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn high-level music requests into structured genre, tempo, instrumentation, vocal, lyric, and generation-command plans for mmx-based music creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external mmx CLI with broad local file access and weak containment.

Mitigation: Use an isolated environment, verify the executable path and source before running commands, and stop if the CLI identity check fails.

Risk: Prompts, lyrics, and reference audio may be sent to the external tool or its service.

Mitigation: Avoid private, sensitive, or unreleased material unless the user has approved that disclosure.

Risk: Generated output paths can affect local files.

Mitigation: Keep output names to simple filenames under the intended output folder.

## Reference(s):

- [Music Composer skill page](https://clawhub.ai/yuhouxinliang/skills/music-composer)
- [MiniMax](https://www.minimax.io)
- [Music Genre & Production Parameters Reference](references/music-genres.md)
- [Lyrics Structure Templates](references/lyrics-structures.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown with prompt text, lyrics, and inline bash commands; mmx may save generated audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted mmx CLI installation and user-provided prompts, lyrics, or reference audio.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
