## Description: <br>
Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content creators use this skill to produce narrated mathematical or educational animations, including Manim scene code, rendering commands, subtitle guidance, and local pipeline steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Manim scene files run as local Python code and can execute with the permissions of the local environment. <br>
Mitigation: Review generated scene files before execution and run them in a project-specific or disposable Python environment. <br>
Risk: Cloud TTS providers can receive narration text when network-based voiceover is used. <br>
Mitigation: Use offline pyttsx3 for private narration and avoid sending secrets or confidential text to cloud TTS services. <br>
Risk: Voiceover media and subtitles can remain in local output or cache directories. <br>
Mitigation: Clear media and voiceover caches after rendering when narration content is sensitive. <br>
Risk: Rendering depends on local Manim, FFmpeg, codec, subtitle, and font support. <br>
Mitigation: Run the provided environment check before rendering and resolve missing Manim, libx264, libass, or font dependencies. <br>


## Reference(s): <br>
- [Manim Animation Technical Guide](references/manim_guide.md) <br>
- [Environment Check Script](scripts/check_environment.py) <br>
- [Render Pipeline Script](scripts/run_pipeline.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local Manim scene files, rendered video outputs, SRT subtitles, and voiceover media caches when the generated workflow is executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
