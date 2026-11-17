## Description:

Phonebridge helps users find beginner-friendly steps for enabling developer mode and USB debugging on common Android phone brands, and for exporting or backing up selected mobile app data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woozakii](https://clawhub.ai/user/woozakii)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get step-by-step phone connection, USB debugging, screen capture, chat export, and backup guidance for their own devices and accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may permit an agent to inspect imported phone data from a broad local folder.

Mitigation: Use local phone-data connectors only when the user intentionally asks the agent to inspect specific exported files, and scope the request to those files.

Risk: Phone exports and backups can contain private account, chat, and device data.

Mitigation: Keep exports private, use trusted computers, and disable USB debugging after the needed transfer or backup is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/woozakii/skills/phonebridge-skill)
- [Server-Resolved GitHub Import](https://github.com/Woozakii/phonebridge/tree/main/phonebridge-skill)
- [Phonebridge Tutorial Site](https://b1f884fbf01f443d9e99f3d71dad32c6.gz4.agentos-app.net)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown instructions with step-by-step paths, FAQ notes, and occasional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remind users to back up data and limit guidance to their own devices and accounts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
