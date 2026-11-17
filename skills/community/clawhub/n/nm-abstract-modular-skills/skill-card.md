## Description:

Build composable skill modules with hub-and-spoke loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers designing, refactoring, or maintaining agent skills use this guidance to split large skills into focused modules, load details progressively, and review structure, token use, and migration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance includes a broad command that reportedly makes every file under scripts/ executable.

Mitigation: Review the permission change and confirm each affected file should be executable before applying it; the security analysis was partial, so inspect the complete referenced paths before following the guidance.

## Reference(s):

- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-abstract-modular-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown guidance with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers modular design, progressive loading, validation, migration, optimization, and troubleshooting.]

## Skill Version(s):

1.10.3 (source: frontmatter; server release metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
