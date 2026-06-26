## Description: <br>
News video maker skill. Use search tools to get news, generate speech, and create video with golden subtitles. For creating news briefing videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iZorro](https://clawhub.ai/user/iZorro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn current news topics into narrated briefing videos with a background image, speech audio, and timed subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search queries and narration text may be sent to configured search and text-to-speech providers. <br>
Mitigation: Use approved providers and avoid including confidential or sensitive information in search queries or narration text. <br>
Risk: The workflow runs FFmpeg against user-provided input paths and output directories to create a local MP4 file. <br>
Mitigation: Use trusted background images, audio, subtitle files, and output directories before executing the generated FFmpeg command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline FFmpeg command examples and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or coordinates news text, TTS audio, SRT subtitles, and a local MP4 video file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
