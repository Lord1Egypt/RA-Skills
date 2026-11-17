## Description:

Searches OpenSubtitles for movie subtitles, downloads subtitle files, parses .srt and .ass dialogue, and helps an agent summarize movie plots from subtitle text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find and download movie subtitles from OpenSubtitles, extract dialogue from local subtitle files, and prepare subtitle text for plot summaries or scene analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded subtitle filenames can influence where files are written and may overwrite local files.

Mitigation: Use an explicit save path inside a dedicated workspace directory and review downloaded filenames before writing files.

Risk: OpenSubtitles credentials, search terms, and subtitle text may be sent to external services.

Mitigation: Use restricted credentials, avoid sensitive search or subtitle content, and review external-service handling before installation.

Risk: Dependency versions are not pinned.

Mitigation: Install in an isolated environment and pin reviewed dependency versions before production use.

## Reference(s):

- [OpenSubtitles API](https://opensubtitles.stoplight.io)
- [pysubs2](https://github.com/Arcanemagus/pysubs2)
- [ClawHub Skill Page](https://clawhub.ai/adminlove520/skills/movie-subtitle-viewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration values, subtitle dialogue text, and plot-summary text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime use requires OpenSubtitles credentials and may create downloaded subtitle files in the workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
