## Description: <br>
Search, download, parse, and summarize movie subtitles from OpenSubtitles in .srt or .ass formats using movie name and year. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to search for movie subtitles, download subtitle files, parse dialogue, and prepare subtitle text for AI-assisted plot summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill follows download links returned by OpenSubtitles without host validation, redirect limits, or response-size limits. <br>
Mitigation: Review before installing and prefer an updated version that validates download hosts, limits redirects and response sizes, and downloads only from expected OpenSubtitles endpoints. <br>
Risk: Downloaded subtitle filenames or paths may write outside a clearly bounded workspace, overwrite files, or allow path traversal. <br>
Mitigation: Download only into a dedicated folder and prefer an updated version that sanitizes filenames, blocks path traversal, and prevents unintended overwrites. <br>
Risk: OpenSubtitles credentials are required and subtitle text may be sent to an AI provider for summarization. <br>
Mitigation: Use a limited OpenSubtitles account, store credentials in a normal secret store, and disclose or review any AI-provider transfer of subtitle text. <br>


## Reference(s): <br>
- [Movie Subtitle Viewer ClawHub listing](https://clawhub.ai/adminlove520/movie-subtitle-viewer) <br>
- [OpenSubtitles API](https://opensubtitles.stoplight.io) <br>
- [pysubs2](https://github.com/Arcanemagus/pysubs2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, environment-variable configuration, parsed subtitle text, and downloaded subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenSubtitles credentials; parses .srt and .ass files; downloaded subtitles are written to the requested save path or source filename.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
