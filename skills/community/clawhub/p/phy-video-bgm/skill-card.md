## Description:

Analyze a video's mood and add AI-generated BGM. Optionally speed up/slow down. Uses Gemini for video analysis and fal.ai Lyria2 for music generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to analyze a local video, generate matching background music, optionally adjust playback speed, and produce a final video with replacement BGM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos may be uploaded to Gemini and fal.ai during analysis and music generation.

Mitigation: Avoid processing sensitive or confidential videos unless those external service transfers are acceptable.

Risk: The produced final video replaces the original audio track with generated background music.

Mitigation: Keep an original copy of any video with important narration or ambient audio before running the workflow.

Risk: The workflow depends on API keys and third-party AI services.

Mitigation: Use a virtual environment, pin dependencies where practical, and provide credentials through environment variables.

## Reference(s):

- [Phy Video Bgm on ClawHub](https://clawhub.ai/phy041/skills/phy-video-bgm)
- [Canlah AI](https://canlah.ai)
- [fal.ai Lyria2 endpoint](https://fal.run/fal-ai/lyria2)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated outputs include WAV and MP4 media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local video input, Gemini and fal.ai API keys, and FFmpeg; generated files are saved beside the input video.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
