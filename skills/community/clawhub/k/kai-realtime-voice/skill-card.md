## Description: <br>
Generates speech audio from text with MiniMax using a configured API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check MiniMax text-to-speech access and generate MP3 speech audio from supplied text. It is suited to voice-output workflows that already have a MiniMax API key configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and text provided to the skill are sent to MiniMax under the user's API key. <br>
Mitigation: Avoid sending secrets or sensitive private content unless MiniMax data handling is acceptable for that material. <br>
Risk: The release describes real-time WebSocket streaming, but the security summary identifies the implementation as a REST-based MP3 generation helper. <br>
Mitigation: Treat the skill as text-to-speech file generation and validate latency or streaming requirements before relying on it for real-time voice workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown instructions with bash commands; runtime output is status text and MP3 audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY. Generated text is sent to MiniMax, and MP3 output is saved under KAI_MINIMAX_WORKSPACE or the default OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
