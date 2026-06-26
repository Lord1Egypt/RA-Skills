## Description: <br>
Music Creator guides an agent through AI-assisted song creation, including lyric writing, MiniMax music and cover generation, lyric timing alignment, LRC output, and deployment of a synchronized music playback page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomtrije](https://clawhub.ai/user/tomtrije) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a requested theme and music style into a complete AI-generated song package with lyrics, cover art, audio, synchronized lyrics, and a shareable playback page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive MiniMax credentials may be exposed through chat prompts, CLI login behavior, or bundled plaintext configuration. <br>
Mitigation: Use a secret manager or temporary token, remove plaintext keys from configuration before use or sharing, and confirm where the MiniMax CLI stores credentials. <br>
Risk: The workflow can install dependencies and run shell commands that change the local environment. <br>
Mitigation: Review each command before execution and prefer isolated project or virtual environments over system-wide installs. <br>
Risk: The deployment step can publish generated music assets to a destination whose visibility depends on another skill's configuration. <br>
Mitigation: Confirm the deployment target, access level, and files to be copied before running deployment commands. <br>


## Reference(s): <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [Music Creator ClawHub Page](https://clawhub.ai/tomtrije/music-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, LRC, HTML, MP3, and JPG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided creative inputs and MiniMax credentials before generation.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
