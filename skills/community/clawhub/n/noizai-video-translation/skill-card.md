## Description: <br>
Translate and dub videos from one language to another, replacing the original audio with TTS while keeping the video intact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ksuriuri](https://clawhub.ai/user/Ksuriuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate video speech into another language, generate dubbed audio, and produce a video with the original visuals preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on an external downloader, the Noiz TTS skill, and the Noiz service. <br>
Mitigation: Install and run it only in environments where those dependencies and service terms are trusted and approved. <br>
Risk: Voice cloning and translated dubbing can be misused or applied to media without proper rights. <br>
Mitigation: Use the skill only for videos, subtitles, and voices the user has permission to translate, clone, and redistribute. <br>
Risk: The Noiz API key may be exposed if stored in repository files or shared project artifacts. <br>
Mitigation: Prefer environment-based secret handling and avoid committing NOIZ_API_KEY or generated credential files. <br>
Risk: Generated output files may overwrite existing video assets when reused filenames are supplied. <br>
Mitigation: Choose a new output filename and review the final path before running the audio replacement step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ksuriuri/noizai-video-translation) <br>
- [youtube-downloader skill repository](https://github.com/crazynomad/skills) <br>
- [youtube-downloader SKILL.md](https://github.com/crazynomad/skills/blob/master/youtube-downloader/SKILL.md) <br>
- [NoizAI TTS skill repository](https://github.com/NoizAI/skills) <br>
- [NoizAI TTS SKILL.md](https://github.com/NoizAI/skills/blob/main/skills/tts/SKILL.md) <br>
- [Noiz API keys](https://developers.noiz.ai/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a final dubbed video file path on success or a clear download, TTS, or audio replacement error on failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
