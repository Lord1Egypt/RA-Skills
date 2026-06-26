## Description: <br>
Native macOS meeting automation for OpenClaw: calendar/window detection, prompt-before-recording, ScreenCaptureKit system audio + microphone recording, local whisper-cli transcription, and agent-generated meeting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nowhitestar](https://clawhub.ai/user/nowhitestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to install and operate a desktop meeting assistant that detects meetings, asks before recording, records microphone and system audio, transcribes locally, and queues meeting-note generation for an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests microphone, system-audio, Accessibility, and optional calendar access, which can expose sensitive meeting and window context. <br>
Mitigation: Install only when those permissions are acceptable, grant the minimum permissions needed, and review configuration before enabling calendar integration. <br>
Risk: Meeting recordings, transcripts, and summaries may contain sensitive content. <br>
Mitigation: Keep output configured to local file storage unless external sharing is intended, and review any LLM, Notion, Telegram, or Zulip configuration before use. <br>
Risk: The security evidence reports sensitive recording and window-inspection controls exposed too broadly for a desktop skill. <br>
Mitigation: Restrict the AudioDaemon socket permissions before use and avoid enabling the public calendar tunnel unless it is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nowhitestar/nowhitestar-meeting-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets; generated meeting notes are written as Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcripts, summary request queue entries, and optional summary delivery instructions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
