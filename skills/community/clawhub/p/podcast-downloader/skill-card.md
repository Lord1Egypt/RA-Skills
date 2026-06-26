## Description: <br>
Downloads podcast audio and show notes from xiaoyuzhoufm.com, converts audio to MP3, and saves the results locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zymclaw](https://clawhub.ai/user/zymclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download Xiaoyuzhou podcast episodes, convert audio for offline playback, and save show notes as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast audio and show notes may be saved to a cloud-synced default folder. <br>
Mitigation: Set PODCAST_DIR to a local, non-synced directory when downloaded content or notes should remain private. <br>
Risk: The original m4a file is deleted by default after MP3 conversion. <br>
Mitigation: Set KEEP_M4A=true when retaining the original source audio is required. <br>
Risk: Downloads and parsing depend on Xiaoyuzhou page structure and external media URLs. <br>
Mitigation: Review failed downloads before retrying and update the script if the site structure changes. <br>


## Reference(s): <br>
- [Podcast Downloader page](https://clawhub.ai/zymclaw/podcast-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/zymclaw) <br>
- [Podcast Downloader Reference](reference.md) <br>
- [Xiaoyuzhou](https://www.xiaoyuzhoufm.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Configuration] <br>
**Output Format:** [Shell commands and local MP3 and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and ffmpeg; output location, MP3 quality, and m4a retention are configurable with environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
