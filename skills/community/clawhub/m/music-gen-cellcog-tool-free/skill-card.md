## Description: <br>
CellCog音乐生成免费版 helps agents guide users through CellCog text-to-music and lyrics-to-music generation with style, duration, voice, and output-format parameters for personal content creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agent users use this skill to draft prompts, parameters, and API calls for CellCog music generation from text descriptions or lyrics. It is best scoped to personal music creation workflows such as background music, short-video tracks, and original song drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises unrelated video, media conversion, automation, API design, and code-generation uses beyond the documented CellCog music-generation workflow. <br>
Mitigation: Use it only for CellCog text-to-music or lyrics-to-music tasks unless the publisher narrows and documents the extra capabilities. <br>
Risk: The skill declares exec/write authority and includes shell command examples that may run in the user's environment. <br>
Mitigation: Review proposed commands before execution and limit writes to expected configuration or output files. <br>
Risk: The workflow requires a CellCog API key. <br>
Mitigation: Provide the key through a private environment variable or local config and do not paste it into shared prompts, logs, or generated artifacts. <br>
Risk: Generated music rights and commercial use may depend on CellCog service terms and platform policies. <br>
Mitigation: Check CellCog terms and the target platform's AI-generated music policy before publishing or monetizing generated audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/music-gen-cellcog-tool-free) <br>
- [CellCog music generation API endpoint](https://api.cellcog.com/v1/music/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference CellCog API credentials and generated MP3 outputs; users should review terms and commands before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
