## Description: <br>
MiniMax Media helps agents generate speech, images, videos, image variations, image-to-video outputs, and music through a unified MiniMax command workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lqqk7](https://clawhub.ai/user/lqqk7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to route MiniMax media requests for text-to-speech, image generation, image editing, video generation, image-to-video generation, and music generation through one command-oriented workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the skill calls a relative MiniMax helper that is not included in the artifact. <br>
Mitigation: Review before installing, provide the missing helper only from a trusted source, and avoid running the skill where an unrelated relative helper could be invoked. <br>
Risk: MiniMax prompts, images, audio, lyrics, and generated media may be sent to an external service. <br>
Mitigation: Use a limited MiniMax API key and avoid submitting sensitive content unless MiniMax data handling terms are acceptable. <br>


## Reference(s): <br>
- [MiniMax API host](https://api.minimaxi.com) <br>
- [ClawHub MiniMax Media release page](https://clawhub.ai/lqqk7/minimax-media) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lqqk7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media files are written to the current working directory or an explicit output path when the helper command is available.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
