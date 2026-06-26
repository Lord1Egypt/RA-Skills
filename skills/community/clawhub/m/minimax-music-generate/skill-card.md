## Description: <br>
MiniMax music generation skill that helps agents generate lyrics, create MP3 music with MiniMax, query task status, and save results locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silingyuan0](https://clawhub.ai/user/silingyuan0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate song lyrics, create MiniMax MP3 music from lyrics and style descriptions, check generation status, and save music outputs to local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The download helper can fetch arbitrary URLs and write to a caller-selected local path. <br>
Mitigation: Use the download command only with trusted MiniMax music URLs and save outputs inside a safe working directory with filenames that may be created or overwritten. <br>
Risk: The skill requires a MiniMax API key for remote API calls. <br>
Mitigation: Use a dedicated MiniMax API key and avoid exposing it in prompts, logs, command history, or shared configuration. <br>


## Reference(s): <br>
- [MiniMax Music API Reference](references/api.md) <br>
- [ClawHub skill release](https://clawhub.ai/silingyuan0/minimax-music-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, command-line output, JSON status data, generated lyrics text, and MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and optional MINIMAX_REGION environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
