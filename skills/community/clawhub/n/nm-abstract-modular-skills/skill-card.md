## Description:

Build composable skill modules with hub-and-spoke loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan, build, and maintain modular agent skills. It provides hub-and-spoke design guidance, example shell commands, and advice for migration, validation, and token efficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance recommends recursively marking every file in a scripts directory executable, which can grant execute permissions to files that do not need them.

Mitigation: Inspect the target files and grant execute permission only to the specific scripts that need it; avoid blanket recursive permission changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-modular-skills)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progressive disclosure through focused skill modules.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
