## Description:

Select and send local reaction GIFs by tag for gestures such as pat-on-back, celebration, salute, and facepalm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirza42](https://clawhub.ai/user/mirza42)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to select a local, tag-matched reaction GIF and include the resulting media path in an agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An editable index or environment override can make the picker emit a MEDIA path for an unintended local file.

Mitigation: Use only trusted index.json, GIF_LIBRARY_INDEX, and GIF_LIBRARY_DIR values, and review emitted MEDIA paths before sending attachments.

Risk: The population script downloads media from network URLs during setup.

Mitigation: Review populate.sh before running it and prefer pinned, reviewed GIF sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirza42/skills/gif-picker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text MEDIA line, listing output, or verification status from a Python CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local filesystem paths to selected GIF files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
