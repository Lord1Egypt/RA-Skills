## Description:

Transcribe audio with Microsoft's MAI-Transcribe-1 model via Azure AI Speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robotsbuildrobots](https://clawhub.ai/user/robotsbuildrobots)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local audio files through an Azure Speech resource and save the result as a plain-text transcript or raw JSON response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are sent to the configured Azure Speech endpoint for processing.

Mitigation: Use the skill only for recordings permitted by the user's Azure data-handling and privacy requirements.

Risk: The skill requires an Azure Speech key and endpoint in environment variables.

Mitigation: Set AZURE_SPEECH_ENDPOINT to the exact HTTPS Speech resource endpoint, protect AZURE_SPEECH_KEY as a cloud credential, and rotate it when needed.

Risk: Large audio files are buffered in memory before upload.

Mitigation: Prefer normal-sized voice recordings or split very large recordings before transcription.

## Reference(s):

- [MAI-Transcribe-1 Azure AI Speech documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-transcribe)
- [ClawHub skill page](https://clawhub.ai/robotsbuildrobots/skills/mai-transcribe)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript or raw JSON response written to a local file, with concise command and setup guidance for the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is the input audio path with .txt appended; --json writes the raw Azure response.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
