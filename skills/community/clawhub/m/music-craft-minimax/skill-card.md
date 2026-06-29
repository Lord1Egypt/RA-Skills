## Description: <br>
Advanced music generation for OpenClaw, using the MiniMax Music 2.6 token plan. Use for cover and style transfer, two-song mashup, lyrics generation API, emotion-driven prompt engineering, and fine control via the `mmx` CLI. Extends `music-craft` with MiniMax-specific features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luischarro](https://clawhub.ai/user/luischarro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and music-production operators use this skill to route MiniMax music requests, analyze local audio, create covers or mashups, generate or edit lyrics, and produce verified generation commands and delivery artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax cloud workflows may send prompts, lyrics, reference audio, and generated-content inputs to MiniMax. <br>
Mitigation: Confirm user consent and authorization before cloud generation, especially for sensitive, private, or third-party-owned audio. <br>
Risk: The workflow requires a MiniMax API key for cloud features. <br>
Mitigation: Install and run it only in environments where handling MINIMAX_API_KEY is acceptable, and avoid exposing the key in prompts, logs, or shared files. <br>
Risk: Remote model code can execute external repository code if enabled for optional analysis. <br>
Mitigation: Do not enable --allow-remote-model-code unless the exact model repository has been reviewed and trusted. <br>
Risk: Generated and analysis artifacts are written to local output paths or temporary directories. <br>
Mitigation: Choose output folders deliberately and rely on the skill's explicit overwrite controls before replacing user-visible files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luischarro/music-craft-minimax) <br>
- [Project homepage](https://github.com/LuisCharro/skills/tree/main/publish/music-craft-minimax) <br>
- [README](README.md) <br>
- [MiniMax generation caveats](references/minimax-generation-caveats.md) <br>
- [Setup and pre-flight](references/setup-and-preflight.md) <br>
- [mmx CLI flag reference](references/mmx-flags-reference.md) <br>
- [Cover workflow](references/cover-workflow.md) <br>
- [Mashup workflow](references/mashup-workflow.md) <br>
- [Lyrics generation](references/lyrics-generation.md) <br>
- [Emotion analysis](references/emotion-analysis.md) <br>
- [Error handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON analysis outputs, prompt text, lyrics files, and generated audio file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY for MiniMax cloud workflows; local analysis writes JSON, lyrics, prompts, temporary media, and generated audio to user-selected paths or temporary directories.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
