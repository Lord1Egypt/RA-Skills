## Description: <br>
HeyVideoGen helps agents create vertical MP4 videos by combining storyboard planning, MiniMax Hailuo AI video clips, HyperFrames HTML and GSAP composition, TTS voiceover, and FFmpeg finalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devioslang](https://clawhub.ai/user/devioslang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to plan short-video storyboards, generate or reference AI video clips, author HyperFrames HTML compositions, and render publishable vertical MP4 assets. It is aimed at workflows that need HTML-based motion graphics, captions, TTS narration, and final video assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper workflow can run shell commands built from user-provided or generated text. <br>
Mitigation: Run it only in a controlled workspace, review generated commands and storyboard values before execution, and update the helper to use validated arguments with shell=False before accepting untrusted inputs. <br>
Risk: The skill requires sensitive credentials for downstream video, TTS, or media-generation providers. <br>
Mitigation: Use limited-scope API keys, keep credentials out of prompts and generated project files, and avoid sending sensitive scripts or proprietary prompts to providers unless that data sharing is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/devioslang/heyvideogen) <br>
- [HyperFrames](https://github.com/heygen-com/hyperframes) <br>
- [HTML authoring guide](references/html-authoring.md) <br>
- [GSAP animation rules](references/gsap-rules.md) <br>
- [Captions and subtitles](references/captions.md) <br>
- [Transitions](references/transitions.md) <br>
- [TTS workflow](references/tts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON storyboard structures, HTML/JavaScript snippets, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local project files and rendered MP4 video assets when the required external tools and credentials are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
