## Description:

Scans macOS and Linux developer storage, identifies likely unused toolchains and caches, and guides users through a confirmation-based cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to understand which development tools, runtimes, caches, and AI-related directories are using disk space on macOS or Linux. It groups findings into data, cache, and likely leftovers, then helps users review cleanup choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup choices may remove active language toolchains or Homebrew versions beyond their descriptions; two scripts were only partially inspected.

Mitigation: Review each target and command, start with `bash scripts/clean.sh --dry-run`, and leave any unclear toolchain or Homebrew item unselected.

## Reference(s):

- [Cleanup classification rules](references/rules.md)
- [Report workflow](references/report.md)
- [Safety boundaries](references/safety.md)
- [Source repository](https://github.com/huiyonghkw/hekouwang-env-doctor-skill)
- [ClawHub release page](https://clawhub.ai/huiyonghkw/skills/hekouwang-env-doctor-skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Disk usage findings grouped as data, cache, and likely leftovers, with reasons and cleanup tradeoffs.]

## Skill Version(s):

1.2.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
