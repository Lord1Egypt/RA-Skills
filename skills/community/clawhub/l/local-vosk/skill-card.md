## Description: <br>
Local Vosk STT provides offline speech-to-text transcription with Vosk for Telegram voice messages and common audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkiwi](https://clawhub.ai/user/sfkiwi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to transcribe Telegram voice notes and local audio files without cloud speech-to-text APIs. It is suited to offline workflows after the Vosk dependency and speech model are installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup asks users to install a local Python package and download a speech model. <br>
Mitigation: Use a virtual environment when possible, verify the model source, and review local package installation before deployment. <br>
Risk: The documented workflow depends on a referenced local transcribe script being present in the installed skill package. <br>
Mitigation: Confirm the transcribe script exists and runs successfully before relying on the skill for operational transcription. <br>


## Reference(s): <br>
- [Local Vosk STT on ClawHub](https://clawhub.ai/sfkiwi/local-vosk) <br>
- [Vosk Models](https://alphacephei.com/vosk/models) <br>
- [Default Vosk English model download](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcription guidance and command examples; transcription quality depends on the installed Vosk model and input audio.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
