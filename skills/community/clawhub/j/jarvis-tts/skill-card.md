## Description: <br>
Jarvis TTS generates natural-sounding Chinese text-to-speech with Microsoft edge-tts and plays it locally with macOS afplay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e421083458](https://clawhub.ai/user/e421083458) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI assistant operators use this skill to convert Chinese text responses, notifications, reminders, or longer passages into spoken audio on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested speech text is sent to Microsoft Edge TTS for audio generation. <br>
Mitigation: Avoid using the skill with secrets, private messages, or confidential business text unless that data handling is acceptable. <br>
Risk: Audio is played on the local macOS machine through afplay. <br>
Mitigation: Run the skill only in environments where local audio playback is appropriate and expected. <br>
Risk: The skill depends on network access, Python 3, edge-tts, and macOS afplay. <br>
Mitigation: Confirm these dependencies and platform assumptions before relying on the skill in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e421083458/jarvis-tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate and play temporary MP3 audio locally when the provided shell or Python script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
