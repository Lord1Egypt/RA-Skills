## Description:

Create mathematical and educational animations with synchronized narration and subtitles using Manim Community and manim-voiceover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators use this skill to draft Manim scene code, configure local rendering, and produce narrated educational videos with optional subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local rendering requires third-party Manim, ffmpeg, and Python dependencies that can fail or vary by environment.

Mitigation: Use a virtual environment or container and run the bundled environment check before rendering.

Risk: Generated Manim scene code and ffmpeg commands execute locally.

Mitigation: Review generated code and commands before execution, especially when handling files or invoking render pipelines.

Risk: The default gTTS narration option can send narration text to Google TTS.

Mitigation: Avoid confidential text in gTTS narration and use the offline pyttsx3 option for sensitive narration.

## Reference(s):

- [Manim Technical Guide](references/manim_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/hzsunzixiang/skills/manim-animation-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Manim scene files, manim.cfg settings, render commands, subtitle guidance, and local pipeline commands.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
