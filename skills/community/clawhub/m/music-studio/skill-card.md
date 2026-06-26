## Description: <br>
Music Studio is a lightweight MiniMax music creation workspace for LLM agents that guides users through generating music, writing lyrics, creating covers, and managing local outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrgyan](https://clawhub.ai/user/mrgyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a conversational MiniMax music studio, including lyric generation, text-to-music generation, cover creation, library management, and local configuration of MiniMax credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax API keys can be saved in local configuration and may also persist in chat setup session history. <br>
Mitigation: Use a dedicated MiniMax API key, prefer the explicit set-key flow, protect ~/.config/music-studio/config.json and output/sessions, and delete setup session files if a key was entered through chat. <br>
Risk: Prompts, lyrics, reference audio URLs, generated audio URLs, and related metadata may be sent to MiniMax and stored locally. <br>
Mitigation: Avoid submitting sensitive or unlicensed material, review MiniMax data handling terms before use, and clean or purge local library and session outputs when they are no longer needed. <br>


## Reference(s): <br>
- [MiniMax Music API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mrgyan/music-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Conversational text with CLI commands and locally written audio, lyric, URL, metadata, library, configuration, and session files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a MiniMax bearer token stored in local configuration; generated prompts, lyrics, reference URLs, audio links, and session history may be stored locally and sent to MiniMax during generation.] <br>

## Skill Version(s): <br>
1.0.10 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
