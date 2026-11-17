## Description:

Generate changelogs from git commit history with conventional commit parsing, grouped output, breaking change detection, and Markdown or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to generate release notes and changelogs from git commit history, including conventional commit groups, breaking changes, and tag or ref ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script reads git commit metadata from repositories the user points it at.

Mitigation: Run it only against intended repositories and review generated changelog content before publication.

Risk: Using -o/--output can replace an existing file at the chosen destination.

Mitigation: Choose the output path explicitly and check whether the destination file should be overwritten before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-changelog-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON changelog content, with shell commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write output to a selected file path when the user passes -o/--output.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
