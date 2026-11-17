## Description:

Search, discover, and install skills from the open agent skills ecosystem to extend agent capabilities for specific tasks or domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isainazar](https://clawhub.ai/user/isainazar)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to find relevant skills, present installation options, and install or update skills through the Skills CLI when extending agent capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or auto-confirmed global skill installs can modify the user's agent environment and future sessions.

Mitigation: Prefer a pinned, trusted Skills CLI version, inspect the source skill before adding it, avoid global auto-confirm installs by default, and require explicit confirmation before install or update commands.

Risk: Broad trigger guidance can cause the skill to recommend discovery or installation during loosely related tasks.

Mitigation: Confirm that the user wants skill discovery before running search commands, and separate discovery from installation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isainazar/skills/openclaw-find-skills)
- [Skills catalog](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed before execution, especially install and update commands that affect future agent sessions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
