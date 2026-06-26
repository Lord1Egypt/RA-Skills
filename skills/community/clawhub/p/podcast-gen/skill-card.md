## Description: <br>
Generates short podcast audio from a user's topic by searching recent information, drafting a conversational script, selecting an XFYUN TTS voice, synthesizing an MP3 under three minutes, and sending the file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn a requested topic into a short podcast-style MP3 using current web search results and XFYUN text-to-speech voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User topics, retrieved facts, and generated podcast script text may be processed by external search or text-to-speech services. <br>
Mitigation: Avoid private, confidential, or regulated topics unless those external-service data flows are acceptable for the use case. <br>
Risk: The skill depends on a separate xfyun-tts skill and XFYUN API credentials. <br>
Mitigation: Install only a trusted xfyun-tts release and provide credentials through OpenClaw or environment configuration rather than hardcoding secrets. <br>
Risk: Search results can be incomplete, promotional, or factually stale before they are converted into audio. <br>
Mitigation: Review the gathered facts, use alternate search sources when results are empty or ad-heavy, and confirm important claims before synthesis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/podcast-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks plus an MP3 file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a temporary script file and MP3 output, then sends the MP3 file after upload succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
