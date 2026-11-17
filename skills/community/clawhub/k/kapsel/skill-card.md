## Description:

Project memory capsules archive completed project knowledge to Google Drive or another rclone-supported cloud remote and reload it on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuwaiapp](https://clawhub.ai/user/nuwaiapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to archive completed project context into structured capsules and reload summaries, details, technical context, or saved files when old project knowledge is needed again.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can execute unintended shell commands through shell-based rclone calls.

Mitigation: Review the script before installation, use only trusted capsule names and file paths, and prefer a patched version that removes shell=True and validates inputs.

Risk: The skill can write or upload project material to configured cloud storage with weak safeguards.

Mitigation: Use only trusted rclone remotes, avoid secrets or regulated data, and require explicit confirmation before uploads or memory changes.

Risk: Local staging paths and user-provided capsule names may not be sufficiently confined.

Mitigation: Configure a dedicated staging directory and avoid untrusted names or files until path handling is constrained.

## Reference(s):

- [rclone documentation](https://rclone.org)
- [rclone installation guide](https://rclone.org/install/)
- [ClawHub skill page](https://clawhub.ai/nuwaiapp/skills/kapsel)
- [ClawHub publisher profile](https://clawhub.ai/user/nuwaiapp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and terminal output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads capsule folders containing summary.md, details.md, context.md, and optional saved files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
