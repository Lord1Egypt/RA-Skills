## Description:

Generates 9:16 vertical short videos from Markdown scripts, with support for automatic scene splitting, audio editing, media conversion, subtitles, and configurable text-to-speech commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and automation teams use this skill to turn Markdown scripts and slide imagery into vertical MP4 short videos with narration, subtitles, and configurable media-processing options. It is intended for content-generation workflows where users control the input script, media assets, and rights to generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The custom TTS command path can give the agent broad local command execution.

Mitigation: Run the skill in a contained environment, review the exact TTS command template before use, and avoid populating command templates from untrusted Markdown or user input.

Risk: The referenced generate.py implementation is not included in the artifact evidence.

Mitigation: Verify the source and behavior of generate.py before allowing it to access files, credentials, media libraries, or production workspaces.

Risk: Video jobs may use API keys and local media files.

Mitigation: Limit credentials and file-system access to the minimum needed for the specific video job and keep keys out of generated assets and version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/lh-video-gen-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-shaped result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to produce or run video-generation commands that create MP4 files and related temporary media assets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
