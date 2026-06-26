## Description: <br>
Percept Listen helps an OpenClaw agent receive ambient conversation transcripts from wearable audio devices, with local storage and searchable speaker-tagged conversation data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when they want an agent to receive locally stored, searchable transcripts from an Omi pendant or Apple Watch audio workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambient listening can capture and store nearby conversations. <br>
Mitigation: Install only when ambient listening is intended, obtain consent from people who may be recorded, and check applicable recording laws. <br>
Risk: Transcript webhooks or tunnels can expose private conversation data if misconfigured. <br>
Mitigation: Protect tunnel and webhook access, and review how local transcript files and the SQLite database are retained or deleted. <br>


## Reference(s): <br>
- [Percept GitHub Repository](https://github.com/GetPercept/percept) <br>
- [Percept Documentation](https://github.com/GetPercept/percept/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/jarvis563/percept-listen) <br>
- [Publisher Profile](https://clawhub.ai/user/jarvis563) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local transcript and conversation file outputs produced by the Percept workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
