## Description: <br>
Transcribe audio with Microsoft's MAI-Transcribe-1 model via Azure AI Speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robotsbuildrobots](https://clawhub.ai/user/robotsbuildrobots) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe user-selected audio files through an Azure Speech resource, producing a local transcript for review or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to Microsoft/Azure for transcription. <br>
Mitigation: Use only audio that is permitted under the user's Azure data handling requirements, and avoid confidential, regulated, or private recordings unless that processing is approved. <br>
Risk: Using the wrong Azure Speech endpoint or key can send requests to an unintended resource or fail authentication. <br>
Mitigation: Verify AZURE_SPEECH_ENDPOINT is the user's own Speech resource endpoint and that AZURE_SPEECH_KEY belongs to that same resource before running transcription. <br>
Risk: Large audio files are buffered in memory before upload. <br>
Mitigation: Prefer normal voice-note-sized recordings or split large recordings before transcription. <br>


## Reference(s): <br>
- [MAI-Transcribe-1 Azure AI Speech documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-transcribe) <br>
- [ClawHub skill page](https://clawhub.ai/robotsbuildrobots/mai-transcribe) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/robotsbuildrobots) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript by default, or raw JSON when requested with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output to a local file, defaulting to <input>.txt or <input>.json.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
