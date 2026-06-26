## Description: <br>
Generate vocal or instrumental music, cover versions, and lyrics through MiniMax music generation APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4833675](https://clawhub.ai/user/4833675) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate songs, instrumental tracks, cover audio, and lyrics from prompts or reference audio through MiniMax services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the setup instructs agents to store a MiniMax API key in local code and documentation files. <br>
Mitigation: Use MINIMAX_API_KEY or a local secret manager, avoid pasting secrets into SKILL.md or generate.py, and review generated configuration before execution. <br>
Risk: Cover generation can upload local reference audio to MiniMax. <br>
Mitigation: Only provide local audio files that the user is willing and authorized to send to MiniMax. <br>


## Reference(s): <br>
- [MiniMax Music Generation Documentation](https://platform.minimaxi.com/docs/guides/music-generation) <br>
- [ClawHub Skill Listing](https://clawhub.ai/skills/minimax-tokenplan-music) <br>
- [ClawHub Release Page](https://clawhub.ai/4833675/minimax-tokenplan-music) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown instructions with CLI examples; runtime output is an audio file path or temporary URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio may be WAV, MP3, or PCM; URL outputs are temporary according to the artifact documentation.] <br>

## Skill Version(s): <br>
0.9.0 (source: frontmatter and changelog, released 2026-04-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
