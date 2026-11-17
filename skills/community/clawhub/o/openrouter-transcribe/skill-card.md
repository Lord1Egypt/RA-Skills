## Description:

Transcribe audio files via OpenRouter using audio-capable models (Gemini, GPT-4o-audio, etc).

This skill is ready for commercial/non-commercial use.

## Publisher:

[obviyus](https://clawhub.ai/user/obviyus)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe local audio files through OpenRouter audio-capable models, with optional model, prompt, output-file, and caller-header settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio recordings are sent to OpenRouter and the chosen model provider for processing.

Mitigation: Use the skill only for audio that is acceptable for third-party processing, and avoid confidential, regulated, or private conversations unless that processing is approved.

Risk: The skill requires an OpenRouter API key.

Mitigation: Provide OPENROUTER_API_KEY through a normal environment variable or approved local configuration, and do not embed secrets in shared files.

## Reference(s):

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [ClawHub skill page](https://clawhub.ai/obviyus/skills/openrouter-transcribe)
- [Publisher profile](https://clawhub.ai/user/obviyus)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript to stdout or a selected output file, plus shell error messages when setup or API calls fail.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, ffmpeg, base64, jq, and OPENROUTER_API_KEY; converts input audio to mono 16 kHz WAV before sending it to OpenRouter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
