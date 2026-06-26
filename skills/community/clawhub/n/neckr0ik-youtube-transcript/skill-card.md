## Description: <br>
Transcribes and extracts subtitles from YouTube videos using yt-dlp so an agent can work with spoken video content as text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neckr0ik](https://clawhub.ai/user/neckr0ik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch YouTube captions or auto-generated subtitles for transcript extraction, summarization, analysis, quoting, or saving to a text file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default-on telemetry sends the user's IP address and usage timing to an author-operated endpoint over plain HTTP. <br>
Mitigation: Review before installing and set DISABLE_TELEMETRY=1 before use if telemetry is not acceptable. <br>
Risk: The skill executes yt-dlp against user-provided YouTube URLs and depends on external network access. <br>
Mitigation: Run in an environment where outbound network access and yt-dlp execution are acceptable for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neckr0ik/neckr0ik-youtube-transcript) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/neckr0ik) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript output, optional transcript file, and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and yt-dlp. Supports a language option and an optional transcript output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
