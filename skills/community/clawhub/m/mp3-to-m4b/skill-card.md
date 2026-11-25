## Description:

Joins a folder of audio files, such as the mp3 parts of an audiobook, into one .m4b with chapters, cover and book tags that Apple Books, BookPlayer and other players read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geragarazagh](https://clawhub.ai/user/geragarazagh)

### License/Terms of Use:

MIT

## Use Case:

People who have audiobook audio split across MP3 or other supported audio files use this skill to combine the parts into a chaptered M4B, using available titles, tags and cover art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some local path references could not be resolved, and the tool scope is undeclared.

Mitigation: Review the skill files and the permissions available in the target environment before running it.

Risk: Using the workflow may require installing ffmpeg.

Mitigation: Install ffmpeg only when needed and after the user approves the installation.

## Reference(s):

- [MP3 to M4B on ClawHub](https://clawhub.ai/geragarazagh/skills/mp3-to-m4b)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [An .m4b audiobook file with chapter metadata and optional cover art, plus concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the new audiobook file; source audio files are left unchanged.]

## Skill Version(s):

0.2.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
