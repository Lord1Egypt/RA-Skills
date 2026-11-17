## Description:

Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and content creators use this skill to generate Manim scene code, render narrated mathematical or educational animations, and optionally produce synchronized subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud TTS providers such as gTTS may process narration text outside the local environment.

Mitigation: Avoid confidential narration with cloud TTS and use the offline pyttsx3 backend when privacy matters.

Risk: Dependency installation can introduce package-source and environment risks.

Mitigation: Install in a virtual environment or container and review package sources before adding optional TTS backends.

Risk: Missing ffmpeg libx264 or libass support can prevent video rendering or subtitle burn-in.

Mitigation: Run the provided environment check before rendering and install an ffmpeg build that includes libx264 and libass.

Risk: Combining in-scene subtitles with SRT burn-in can create overlapping subtitle layers.

Mitigation: Choose either in-scene subtitles or SRT burn-in for a given video, not both.

## Reference(s):

- [Manim Animation Technical Guide](references/manim_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/hzsunzixiang/skills/manim-animation-en)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, INI, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Manim scene files, manim.cfg settings, render commands, subtitle workflow guidance, and environment-check instructions.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
