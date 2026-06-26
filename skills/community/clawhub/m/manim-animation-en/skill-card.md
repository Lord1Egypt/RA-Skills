## Description: <br>
Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content creators use this skill to generate Manim scene code, rendering commands, and subtitle workflows for narrated mathematical or educational videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Manim scenes and pipeline commands run local Python, Manim, and ffmpeg tooling. <br>
Mitigation: Review generated scene files and commands before rendering, and run them in a controlled workspace with expected dependencies installed. <br>
Risk: Default gTTS voiceover can send narration text to Google TTS, which may be unsuitable for confidential or regulated content. <br>
Mitigation: Use the offline pyttsx3 option for sensitive scripts or regulated content. <br>
Risk: Rendered media, subtitles, and voiceover caches may retain sensitive narration or visual content. <br>
Mitigation: Clear generated media and voiceover cache files after sensitive projects. <br>


## Reference(s): <br>
- [Manim Animation Technical Guide](references/manim_guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/hzsunzixiang/manim-animation-en) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local Manim scene files, video render commands, subtitles, and ffmpeg post-processing steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
