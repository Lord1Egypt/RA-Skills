## Description: <br>
Make phone calls through the macOS Phone/FaceTime app and let an OpenClaw agent speak into the call via local TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexrox](https://clawhub.ai/user/flexrox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users on macOS use this skill to place outbound calls through the local Phone/FaceTime Continuity stack and speak generated text into an active call. It is intended for cases where the user has provided an explicit phone number and permission to call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls from the user's Mac/iPhone setup. <br>
Mitigation: Require explicit user permission and a confirmed E.164 phone number before live use; use --dry-run or --no-confirm when manual control is preferred. <br>
Risk: The skill requires macOS Accessibility/Automation permission to control local Phone/FaceTime UI. <br>
Mitigation: Grant permissions only to a trusted OpenClaw runner or terminal process and review the skill before deployment. <br>
Risk: Optional ElevenLabs TTS uses sensitive credentials and may send spoken text to an external service. <br>
Mitigation: Leave ElevenLabs credentials unset when speech should remain local; the skill falls back to macOS say. <br>


## Reference(s): <br>
- [Apple Phone User Guide for Mac](https://support.apple.com/guide/phoneapp/make-or-receive-calls-phn28c9d643a/mac) <br>
- [ClawHub Phone Call release page](https://clawhub.ai/flexrox/phone-call) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and plain text passed to local TTS] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires Phone or FaceTime, osascript, Accessibility/Automation permission, and explicit user permission for live outbound calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
