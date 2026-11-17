## Description:

Package the workspace notes directory into a named ZIP archive with integrity validation, entry counting, and no network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymous9n23](https://clawhub.ai/user/anonymous9n23)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill after notes-sync to package workspace notes into a local retention archive before notes-upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unchecked archive name could cause deletion of an unrelated file.

Mitigation: Check both configured paths, keep a separate backup, and prefer a destination confined to the intended archive location; preserve the previous backup until its replacement passes validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anonymous9n23/skills/notes-pack-rich)
- [Publisher profile](https://clawhub.ai/user/anonymous9n23)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [ZIP archive and plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local, offline archive with reported size and entry count.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
