## Description: <br>
Automatically cuts long poker tournament videos into complete hand clips in vertical 9:16 format with subtitles and short-form hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolenovan](https://clawhub.ai/user/nicolenovan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agents working with poker media use this skill to turn long local tournament videos into short, publishable clips with subtitles, hooks, and clip metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates clips, transcript caches, subtitle files, and JSON reports that may contain private source-media content. <br>
Mitigation: Run it only on intended local video paths, review generated outputs before sharing, and delete clips, transcripts, subtitles, and reports when the media is private or disk usage matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicolenovan/pokerclip) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Workspace files including MP4 clips, ASS subtitles, transcript JSON, clip analysis JSON, and a publish report, with concise command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local video path, Python 3.10+, ffmpeg, and openai-whisper; GPU acceleration is recommended for faster transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
