## Description: <br>
Generates speech with the Jiuma AI API using a selected online voice or a user-provided reference audio sample for voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create TTS audio or clone a permitted voice by sending text and either a Jiuma timbre ID or a reference audio file to Jiuma. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text and optional reference voice audio to Jiuma for TTS or voice cloning. <br>
Mitigation: Use it only with text and voice samples you are comfortable sending to Jiuma, and only clone voices you own or have permission to use. <br>
Risk: Login can save a sensitive Jiuma API key locally. <br>
Mitigation: Treat the saved key as a secret, avoid shared workspaces, and delete or rotate it when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddcn1/jiuma-free-voice-clone) <br>
- [LOGIN.md](LOGIN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status objects with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns generated audio URLs and may write a local voice cache or saved Jiuma API key after login.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
