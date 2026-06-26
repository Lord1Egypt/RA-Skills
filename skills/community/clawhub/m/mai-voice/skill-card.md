## Description: <br>
Synthesize speech with Microsoft's MAI-Voice-1 voices via Azure AI Speech REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robotsbuildrobots](https://clawhub.ai/user/robotsbuildrobots) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to synthesize text into MAI-Voice-1 speech through Azure AI Speech, with configurable voice, style, output path, and audio format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Microsoft Azure Speech. <br>
Mitigation: Avoid submitting secrets, credentials, regulated data, or confidential text unless policy permits Azure processing. <br>
Risk: The skill requires an Azure Speech key. <br>
Mitigation: Store and rotate AZURE_SPEECH_KEY as an API secret and avoid printing or committing it. <br>
Risk: MAI-Voice-1 availability may depend on Azure preview support and resource region. <br>
Mitigation: Use a supported Azure Speech region and verify that the Speech resource supports MAI-Voice-1 before relying on the output. <br>


## Reference(s): <br>
- [MAI voices documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-voices) <br>
- [ClawHub skill page](https://clawhub.ai/robotsbuildrobots/mai-voice) <br>
- [Publisher profile](https://clawhub.ai/user/robotsbuildrobots) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; the script writes an audio file and prints its path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, AZURE_SPEECH_KEY, and AZURE_SPEECH_REGION.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
