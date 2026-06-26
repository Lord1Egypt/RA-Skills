## Description: <br>
Meeting Assistant joins Google Meet, Zoom, or Teams meetings as an AI participant to capture audio and chat, provide real-time transcription, answer meeting-chat questions, and generate meeting summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-G](https://clawhub.ai/user/zeron-G) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and meeting operators use this skill to let an agent join supported remote meetings, monitor transcript and chat activity, send AI-assisted replies, and produce meeting notes. It also includes a medical-assistant mode for summarizing and explaining medical consultations, which requires human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records, transcribes, analyzes, and stores sensitive meeting content. <br>
Mitigation: Use only with explicit participant consent, disable recording or transcription when it is not needed, and define retention and deletion rules for recordings, transcripts, screenshots, logs, and summaries. <br>
Risk: Bundled configuration and documentation include live-looking tokens or credentials. <br>
Mitigation: Replace and rotate all bundled tokens and secrets before use, and keep production credentials outside the skill package. <br>
Risk: Local services and meeting-bot APIs can capture or post broader meeting content than users expect. <br>
Mitigation: Restrict local service ports, limit API access to trusted users, and review chat-posting behavior before joining real meetings. <br>
Risk: Medical mode can generate live explanations or summaries in a high-stakes context. <br>
Mitigation: Use medical mode only as an assistive note-taking workflow and require review by a qualified human before acting on medical content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zeron-G/meeting-assistant-eva) <br>
- [Developer Documentation](docs/README.md) <br>
- [Architecture Overview](docs/architecture.md) <br>
- [Setup Guide](docs/setup.md) <br>
- [Agent Usage Guide](docs/agent-usage.md) <br>
- [API Reference](docs/api-reference.md) <br>
- [Troubleshooting Guide](docs/troubleshooting.md) <br>
- [Integration Guide](references/integration-guide.md) <br>
- [Medical Terms Guide](references/medical-terms-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Meeting chat messages, JSON transcripts and logs, screenshots, audio recordings, and Markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive meeting content and should be retained only under an explicit retention and deletion policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
