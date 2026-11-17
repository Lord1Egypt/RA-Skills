## Description:

Send images from Mac to phone via iMessage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzyyyyyyyy](https://clawhub.ai/user/wzyyyyyyyy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send image files from a Mac to a configured phone number via the Messages app/iMessage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send images through Messages, which may expose files to the wrong recipient.

Mitigation: Require explicit confirmation before each send and show the recipient and image path before Messages is invoked.

Risk: Crafted recipient or file path input could alter the AppleScript command and run unintended local actions.

Mitigation: Pass AppleScript arguments safely, escape values correctly, and validate phone numbers and image paths before sending.

Risk: Copied images are retained in ~/Pictures/openclaw-send/ after sending.

Mitigation: Define a retention policy, clean up copied files after successful sends, or ask the user before retaining copies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wzyyyyyyyy/skills/images-sender)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies images to ~/Pictures/openclaw-send/ before sending through Messages.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
