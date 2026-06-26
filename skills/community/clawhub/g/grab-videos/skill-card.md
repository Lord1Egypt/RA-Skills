## Description: <br>
Download videos and extract frames using yt-dlp and ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and automation agents use this skill to prepare commands for downloading supported videos and extracting frames, thumbnails, clips, or converted media with yt-dlp and ffmpeg. Users should apply it only to media they are allowed to download or process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may overwrite local output files during batch extraction or when overwrite flags are used. <br>
Mitigation: Run in a dedicated working folder, inspect output filenames first, and avoid overwrite flags unless replacement is intended. <br>
Risk: Downloading media without the necessary rights can violate site terms or copyright obligations. <br>
Mitigation: Use the skill only for media the user has permission to download or process. <br>
Risk: Installing media tooling from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install yt-dlp and ffmpeg only from trusted package managers or official project download locations. <br>
Risk: Video downloads can consume significant local storage, especially in batch workflows. <br>
Mitigation: Use bounded output directories and lower-resolution format selectors when storage use matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qidu/grab-videos) <br>
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for local files and external media URLs; commands may create or overwrite video, image, thumbnail, and clip files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
