## Description: <br>
Automate Google Voice calls with AI-generated voice (TTS) or local audio injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to place Google Voice calls from natural-language requests, injecting AI-generated speech or local audio into the call flow. <br>

### Deployment Geography for Use: <br>
Global, subject to Google Voice availability and local calling, consent, and recording rules. <br>

## Known Risks and Mitigations: <br>
Risk: The release includes Google session cookies. <br>
Mitigation: Do not use the bundled cookies; revoke exposed sessions and require each user to provide their own securely stored credentials. <br>
Risk: The skill can place automated phone calls and inject spoken audio. <br>
Mitigation: Require explicit confirmation before every call and verify the destination number and message or audio content before dialing. <br>
Risk: Call audio may be recorded and saved under /tmp. <br>
Mitigation: Treat recordings as sensitive data, obtain required consent, restrict access, and apply a retention or deletion policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joe12801/google-voice-caller) <br>
- [Google Voice calls interface](https://voice.google.com/u/0/calls) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text status output with an optional MP3 recording file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary audio and recording files under /tmp during call execution.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
