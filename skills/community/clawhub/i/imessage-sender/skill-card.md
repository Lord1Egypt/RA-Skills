## Description:

Send images from Mac to phone via iMessage

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzyyyyyyyy](https://clawhub.ai/user/wzyyyyyyyy)

### License/Terms of Use:


## Use Case:

Developers and end users on macOS use this skill to configure a recipient and send local image files through the Messages app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit local image files through Messages to a configured or supplied recipient.

Mitigation: Require explicit recipient and file confirmation before sending, and avoid using it for sensitive files.

Risk: Unsafe AppleScript construction could allow crafted recipient or path values to alter the generated script.

Mitigation: Validate image paths and recipients, and pass AppleScript values as arguments instead of interpolating strings.

Risk: The script stages copied images under ~/Pictures/openclaw-send/.

Mitigation: Review or clean staged copies after sending.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a local Python script that copies images before sending them with Messages on macOS.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
