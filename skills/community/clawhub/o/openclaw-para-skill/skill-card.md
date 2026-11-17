## Description:

Organize files and projects using the PARA method (Projects, Areas, Resources, Archives).

This skill is ready for commercial/non-commercial use.

## Publisher:

[alitekin1](https://clawhub.ai/user/alitekin1)

### License/Terms of Use:


## Use Case:

Developers and workspace users use this skill to keep files and projects organized under PARA categories for active projects, ongoing areas, reference resources, and archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to actively enforce PARA organization and move workspace files.

Mitigation: Require the agent to show proposed moves and get confirmation before moving files.

Risk: Automatic file moves can affect active, configuration, hidden, or important files without rollback safeguards.

Mitigation: Avoid overwrites, exclude active/config/hidden files unless explicitly approved, and keep a move log or rollback plan.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown text with proposed file-organization actions and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform file moves when the agent is allowed to operate on the workspace.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
