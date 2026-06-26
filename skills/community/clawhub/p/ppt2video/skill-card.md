## Description: <br>
Convert PowerPoint presentations into narrated videos with Chinese voiceover, synchronized subtitles, and page-by-page audio sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn uploaded PPT files into Chinese narrated explainer, training, or course videos with per-slide audio and subtitle synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media conversion and text-to-speech dependencies may introduce supply-chain or runtime risk if installed from untrusted sources. <br>
Mitigation: Install required media and TTS tools from trusted sources and pin versions where practical. <br>
Risk: Presentation contents may be exposed to a TTS provider or rendering environment that is not approved for confidential material. <br>
Mitigation: Avoid using confidential presentations unless the TTS provider and rendering environment are approved for that content. <br>
Risk: Slide exports, narration, and frame counts can drift, causing subtitles or page changes to fall out of sync. <br>
Mitigation: Generate audio per slide, measure each clip duration with ffprobe, and set each page duration from the measured frame count before rendering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/ppt2video) <br>
- [Publisher profile](https://clawhub.ai/user/jeffli2002) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, Bash, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides creation of MP4 video output with H.264 video, AAC audio, 854x480 resolution, 24 fps, and embedded subtitles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
