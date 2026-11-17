## Description:

Helps developers synchronize and publish skills and agents across Gitee, GitHub, ClawHub, SkillHub, and PyPI, including releases and file filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers and release maintainers use this skill to synchronize skill and agent projects, prepare packages, and publish updates and releases to configured repositories and registries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing untrusted skills or agents can execute injected commands in the ClawHub shell or generated PyPI package setup.

Mitigation: Do not use these release paths on untrusted content until the command injection issues are fixed; review what will be published.

Risk: The tool changes local Git credential-helper settings during publishing.

Mitigation: Review credential-helper changes and their scope before use, and run only with credentials intended for the target repositories.

## Reference(s):

- [ClawHub git-sync release](https://clawhub.ai/ldxs001/skills/git-sync)
- [Usage guide](references/guide.md)
- [Permissions and access](references/permissions.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown with shell commands; publication can create ZIP archives and indexes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publication and release creation require configured credentials and network access.]

## Skill Version(s):

2.48.0 (source: skill frontmatter, release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
