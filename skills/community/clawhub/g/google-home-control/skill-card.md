## Description:

Control smart home devices (lights, TV, etc.) via the Google Assistant SDK. Use when the user wants to trigger home automation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tvdofficial](https://clawhub.ai/user/tvdofficial)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent execute Google Assistant text commands for linked smart home devices after configuring Google Cloud OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent persistent access to local Google OAuth credentials and authority to send real commands to linked smart home devices.

Mitigation: Use a dedicated Google project or account where possible, isolate the OAuth credential file, and require explicit confirmation before device-changing commands.

Risk: Smart home actions may affect physical devices with limited guardrails once credentials are available.

Mitigation: Install only in a trusted local environment, pin dependencies, and review requested commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tvdofficial/skills/google-home-control)
- [Google Cloud Console](https://console.developers.google.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown setup guidance and plain text command responses from the control script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google OAuth credentials and Google Assistant SDK dependencies.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
