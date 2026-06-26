## Description: <br>
Chat with a real person or fictional character in a generated voice by finding public speech online, extracting a clean reference sample, generating audio replies, or designing a voice from an uploaded image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ksuriuri](https://clawhub.ai/user/Ksuriuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to roleplay or converse with public figures or fictional characters using synthetic speech. The skill supports name-based voice cloning from public online media and image-based voice design when a person is not recognizable from name alone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can imitate real-person voices and could be misused for deception, harassment, defamation, or undisclosed synthetic speech. <br>
Mitigation: Use only for consented, lawful, clearly disclosed synthetic-audio scenarios; decline requests targeting private individuals or harmful impersonation. <br>
Risk: The workflows may download public speech, upload images or descriptions to Noiz, use a Noiz API key, and store generated voice artifacts locally. <br>
Mitigation: Keep the default Noiz endpoint, protect the NOIZ_API_KEY value, disclose third-party uploads, and delete local outputs that should not be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Ksuriuri/noizai-chat-with-anyone) <br>
- [Publisher profile](https://clawhub.ai/user/Ksuriuri) <br>
- [Noiz API base URL](https://noiz.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, audio files, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and generated WAV file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local MP3, SRT, WAV, preview audio, and voice_id.txt files under tmp/chat_with_anyone.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
