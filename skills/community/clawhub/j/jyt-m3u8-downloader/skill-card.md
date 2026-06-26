## Description: <br>
Downloads videos from M3U8/HLS streaming URLs by parsing playlists, downloading TS segments concurrently, handling AES-128 keys, and merging segments into MP4 files with ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jyt2018](https://clawhub.ai/user/jyt2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to download authorized HLS video from M3U8 playlists, including nested playlists and AES-128 encrypted streams, and save the result as an MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader disables HTTPS certificate validation while retrieving playlists, segments, and keys. <br>
Mitigation: Use only trusted M3U8 sources, avoid hostile or public networks, and review the source URL before running downloads. <br>
Risk: Downloaded media and keys are processed by ffmpeg after retrieval from remote sources. <br>
Mitigation: Keep ffmpeg updated and use the skill only with media sources the user is authorized to access and trusts. <br>
Risk: Cleanup removes temporary TS, key, and M3U8 files for the selected output name after a size check. <br>
Mitigation: Use a new dedicated output name or folder for each download so cleanup cannot remove preexisting temporary files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jyt2018/jyt-m3u8-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/jyt2018) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can produce an MP4 file plus temporary TS, key, and M3U8 files during download and merge operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
