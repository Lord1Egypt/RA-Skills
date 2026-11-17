## Description:

Manages OpenClaw skills by listing installed skills, summarizing their functions, and identifying overlapping capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damiencronw](https://clawhub.ai/user/damiencronw)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to inventory installed skills, understand their purposes, and spot duplicated functionality across local and ClawHub-installed skill sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the helper inspects local OpenClaw skill folders and prints installed skill information.

Mitigation: Run it only in environments where exposing the local skill inventory in terminal output is acceptable.

Risk: The helper executes `clawhub list`, so results depend on the installed ClawHub CLI and its current authentication or configuration.

Mitigation: Use a trusted ClawHub CLI installation and review CLI behavior before running the helper in shared or sensitive environments.

Risk: Some documented capabilities, such as category display, appear incomplete in the inspected script.

Mitigation: Validate the helper behavior before relying on categorized or duplicate-skill reporting, and update the script or documentation if those workflows are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/damiencronw/skills/openclow-skill-manager)
- [ClawHub Publisher Profile](https://clawhub.ai/user/damiencronw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local OpenClaw skill folders and call the ClawHub CLI when the helper script is run.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
