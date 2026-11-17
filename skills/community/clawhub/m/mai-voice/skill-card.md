## Description:

Synthesize speech with Microsoft's MAI-Voice-1 voices via Azure AI Speech REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robotsbuildrobots](https://clawhub.ai/user/robotsbuildrobots)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize text into MAI-Voice-1 speech through Azure AI Speech, selecting supported voices, optional speaking styles, output format, and destination MP3 path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Azure Speech key and user text to an endpoint built from the AZURE_SPEECH_REGION environment variable.

Mitigation: Set AZURE_SPEECH_REGION only from a trusted Azure resource value and add region validation before shared or automated use.

Risk: Speech input may contain secrets, regulated personal data, or other sensitive text that would be sent to Azure Speech.

Mitigation: Avoid submitting secrets or regulated personal data, and review data-handling requirements before using real credentials.

## Reference(s):

- [Microsoft MAI voices documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-voices)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files]

**Output Format:** [Shell commands with environment variables and a generated MP3 file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure Speech credentials and writes MP3 audio to the requested output path.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
