## Description:

Manage MiniMax Speech 2.8 TTS requests, voice catalog lookups, and precise voice/audio configuration using MiniMax API via CLI or script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingchiu](https://clawhub.ai/user/wingchiu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create MiniMax Speech 2.8 text-to-speech audio, inspect MiniMax voice catalogs, and tune voice, pronunciation, and audio settings through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send MiniMax API keys and requested text to a custom endpoint.

Mitigation: Use only trusted MiniMax endpoints and avoid custom --endpoint values unless the destination is fully trusted.

Risk: The skill can fetch audio from URLs returned by the API when URL output is enabled.

Mitigation: Avoid --output-format url in sensitive environments and prefer hex or base64 payloads when possible.

Risk: The skill requires a MiniMax API key for API requests.

Mitigation: Use a least-privileged or disposable MiniMax key and rotate it after testing or untrusted use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wingchiu/skills/minimax-speech)
- [MiniMax Speech 2.8 T2A API endpoint](https://api.minimax.io/v1/t2a_v2)
- [MiniMax voice catalog API endpoint](https://api.minimax.io/v1/get_voice)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown with inline bash commands and CLI-generated audio or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and sends requested text to the configured MiniMax-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
