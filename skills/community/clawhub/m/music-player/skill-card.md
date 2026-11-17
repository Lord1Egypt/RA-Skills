## Description:

Provides Windows-focused music search, high-quality download, ID3 metadata embedding, and local playback using multiple music API sources.

This skill is for research and development only.

## Publisher:

[freebook8](https://clawhub.ai/user/freebook8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to search for tracks, download selected music files, embed metadata, and launch local playback on Windows. It is best suited for personal learning and development workflows around music file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install steps use mutable or unpinned Python dependencies.

Mitigation: Prefer a pinned skill release, pin Python dependencies in a dependency file, and remove unused dependencies before installation.

Risk: Music downloads write files to local paths and could overwrite important files if pointed at a broad directory.

Mitigation: Save downloads only to a dedicated music folder and review target paths before running download commands.

Risk: The skill depends on external music API sources whose availability and responses can vary.

Mitigation: Review the configured API sources before use and handle failed or unexpected responses before relying on downloaded files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freebook8/skills/music-player)
- [go-music-api](https://github.com/caorushizi/go-music-api)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python script references, and generated local audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create MP3 files and ID3 metadata in user-selected or default music folders.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, README, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
