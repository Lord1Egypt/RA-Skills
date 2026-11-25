## Description:

Helps developers inspect macOS and Linux development environments, classify tool storage as data, cache, or likely leftovers, and review user-confirmed official cache cleanup options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to inspect development-tool storage on macOS and Linux, distinguish active data, caches, and likely leftovers, and decide what to clean. It provides manual guidance for likely leftover version managers and routes cache cleanup through individually confirmed official commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is incomplete: one script was only partially inspected.

Mitigation: Review the skill scripts before use; inspect cleanup options with --dry-run and confirm each selected command individually.

Risk: Official cache cleanup can remove cached packages or downloads that may need to be fetched again.

Mitigation: Review the listed command and its stated cost for each item, and select only caches you are willing to rebuild.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huiyonghkw/skills/hekouwang-env-doctor-skill)
- [GitHub repository](https://github.com/huiyonghkw/hekouwang-env-doctor-skill)
- [Safety boundaries](references/safety.md)
- [Classification rules](references/rules.md)
- [Report format](references/report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only scan guidance; cleanup requires item-by-item user confirmation.]

## Skill Version(s):

1.3.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
