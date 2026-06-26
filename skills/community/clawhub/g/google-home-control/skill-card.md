## Description: <br>
Control smart home devices (lights, TV, etc.) via the Google Assistant SDK. Use when the user wants to trigger home automation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TVDOfficial](https://clawhub.ai/user/TVDOfficial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent send Google Assistant text commands that control linked smart home devices such as lights, TVs, and appliances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Google Assistant control over linked home devices using persistent Google OAuth credentials. <br>
Mitigation: Configure it only on a trusted machine and Google account, protect or revoke the OAuth credential when needed, and restrict use to devices and actions the user is comfortable delegating. <br>
Risk: Commands may affect safety-sensitive devices such as appliances, locks, thermostats, or security equipment. <br>
Mitigation: Add confirmation rules, device allowlists, and action limits before allowing the agent to operate safety-sensitive devices. <br>


## Reference(s): <br>
- [Google Home Control on ClawHub](https://clawhub.ai/TVDOfficial/google-home-control) <br>
- [Google Cloud Console](https://console.developers.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Text] <br>
**Output Format:** [Markdown setup guidance and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Google OAuth credentials and sends text queries to the Google Assistant SDK.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
