## Description: <br>
Manage MiniMax Speech 2.8 TTS requests, voice catalog lookups, and precise voice/audio configuration using the MiniMax API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingchiu](https://clawhub.ai/user/wingchiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to synthesize speech with MiniMax Speech 2.8, inspect available voices, and tune voice and audio settings from a CLI or reusable Python helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TTS text and the MiniMax API key are used in requests to MiniMax. <br>
Mitigation: Use the skill only when MiniMax terms are acceptable, avoid confidential text unless approved, and keep the API key in the MINIMAX_API_KEY environment variable. <br>
Risk: Endpoint overrides can send requests to an unintended service or region. <br>
Mitigation: Use the default MiniMax endpoint or a verified MiniMax regional endpoint before running the CLI. <br>
Risk: The CLI writes audio or JSON output to the path provided by the user. <br>
Mitigation: Choose output paths deliberately and review commands before execution to avoid overwriting important files. <br>
Risk: The helper depends on the Python requests package. <br>
Mitigation: Install requests from a trusted package source in the environment that will run the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wingchiu/minimax-speech) <br>
- [MiniMax T2A API endpoint](https://api.minimax.io/v1/t2a_v2) <br>
- [MiniMax voice catalog API endpoint](https://api.minimax.io/v1/get_voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python CLI usage; the bundled script can emit audio files or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and network access to MiniMax endpoints; TTS writes audio files and voice lookup can write JSON catalogs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
