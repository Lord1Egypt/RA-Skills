## Description: <br>
Play TTS or audio on the Raspberry Pi (or gateway host) default speaker. Use when the user asks for an announcement, alarm, news summary, or "say X on the Pi speaker" and the gateway runs on a Pi (or host with local audio). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noBloodOnTheLeaves](https://clawhub.ai/user/noBloodOnTheLeaves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use this skill to generate short spoken announcements or audio playback on a Raspberry Pi or gateway host speaker after TTS output is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated speech or audio may disclose information to people near the speaker. <br>
Mitigation: Keep announcement text short, avoid sensitive content, and use this skill only where local speaker output is appropriate. <br>
Risk: Playback requires host-level access to local audio tools and files. <br>
Mitigation: Scope execution to paplay, pw-play, or the included helper script, and avoid unnecessary elevated shell access. <br>
Risk: An agent may incorrectly claim audio played before local playback succeeds. <br>
Mitigation: Report success only after the playback command exits successfully; otherwise surface the playback error. <br>


## Reference(s): <br>
- [Pi Speaker ClawHub page](https://clawhub.ai/noBloodOnTheLeaves/pi-speaker) <br>
- [Raspberry Pi audio setup](/platforms/raspberry-pi-audio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio playback binary such as paplay or pw-play and a valid audio file path on the gateway host.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
