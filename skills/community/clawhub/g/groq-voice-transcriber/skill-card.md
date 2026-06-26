## Description: <br>
Automatically transcribes Telegram voice messages with Groq Whisper and returns a Groq LLM-generated text response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Iosif2321](https://clawhub.ai/user/Iosif2321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to process Telegram voice messages by sending audio to Groq Whisper for transcription, then sending the transcript to a Groq-hosted LLM for a concise Russian-language response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram voice audio and generated transcripts may contain sensitive content and are sent to Groq-hosted AI services. <br>
Mitigation: Use the skill only in Telegram chats where participants understand this data flow and avoid processing sensitive audio unless that sharing is intended. <br>
Risk: The artifact includes a hardcoded fallback Groq API key. <br>
Mitigation: Remove the fallback key and require an explicit GROQ_API_KEY so the skill fails closed when no approved key is configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Iosif2321/groq-voice-transcriber) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Plain text response with Python handler code and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROQ_API_KEY and sends Telegram voice audio plus derived transcripts to Groq-hosted services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
