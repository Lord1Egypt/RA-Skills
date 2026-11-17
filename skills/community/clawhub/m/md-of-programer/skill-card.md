## Description:

Insert mind maps and architecture diagrams into Markdown documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drunkpig](https://clawhub.ai/user/drunkpig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to add generated mind maps and architecture diagrams to Markdown documentation while keeping diagram sources and image references organized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad diagram requests.

Mitigation: Confirm the target Markdown file and diagram intent before applying the workflow.

Risk: The skill can install an unpinned global npm package.

Mitigation: Install and pin mddoc-cli in a project-local environment before invoking the skill.

Risk: The skill uses Bash commands and local Markdown edits.

Mitigation: Run it only in workspaces where command execution and persistent documentation changes are acceptable, then review generated files before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drunkpig/skills/md-of-programer)
- [D2 installation documentation](https://d2lang.com/tour/install)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown edits with diagram source files and generated PNG references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .mddoc diagram source files and embeds generated PNG paths into Markdown.]

## Skill Version(s):

0.1.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
