## Description: <br>
Control the iPlay media player to play videos or streams from URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saltpi](https://clawhub.ai/user/saltpi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to open media URLs, streams, or direct video links in the locally installed iPlay desktop app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-provided media URLs in the local iPlay desktop app. <br>
Mitigation: Treat media links as untrusted and run the skill only for links the user intends to open. <br>
Risk: On Windows, the helper currently invokes the platform launcher through shell=True. <br>
Mitigation: Windows users should prefer a future version that avoids shell=True for stronger hardening. <br>


## Reference(s): <br>
- [iPlay Homepage](https://iplay.saltpi.cn) <br>
- [ClawHub skill page](https://clawhub.ai/saltpi/iplay) <br>
- [Publisher profile](https://clawhub.ai/user/saltpi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Command invocation and plain-text status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends a base64-encoded media URL to the local iPlay app through the iplay:// URI scheme; playback status is not monitored.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
