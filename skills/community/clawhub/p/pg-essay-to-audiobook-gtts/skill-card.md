## Description: <br>
Google Text-to-Speech (gTTS) guidance for converting text into audio for audiobooks, podcasts, and speech synthesis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate Python and shell guidance for converting text into MP3 speech, including long-form audiobook workflows that chunk text and concatenate audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is processed by Google's online service. <br>
Mitigation: Use the skill only for non-sensitive text unless the user accepts that service processing; choose an offline text-to-speech tool for secrets, private messages, confidential documents, or regulated personal data. <br>
Risk: The workflow depends on network access and may encounter service availability or rate-limit issues. <br>
Mitigation: Handle network failures gracefully, retry where appropriate, and split long documents into bounded chunks before generating audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/pg-essay-to-audiobook-gtts) <br>
- [Publisher profile](https://clawhub.ai/user/lnj22) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include text-to-speech implementation guidance, installation commands, chunking logic, and audio concatenation examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
