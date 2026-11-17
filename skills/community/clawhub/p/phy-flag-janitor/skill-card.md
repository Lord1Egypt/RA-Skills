## Description:

Phy Flag Janitor helps agents audit local source and configuration files for stale, permanently enabled or disabled, undefined, and unreferenced feature flags, then produce prioritized cleanup guidance with code locations and confirmation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to identify stale feature flags, compare code references with configuration, and plan cleanup work before removing dead branches or flag entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local source, configuration files, .env-style feature-flag entries, and git history for the selected project.

Mitigation: Run it only in intended workspaces and review the scope before sharing generated reports.

Risk: Cleanup recommendations and commands can affect source code, environment examples, or flag configuration if applied without review.

Mitigation: Review proposed removals, confirm production intent, and run the relevant test suite before committing changes.

Risk: Reports can expose internal flag names, code locations, environment variable names, and rollout assumptions.

Mitigation: Treat generated reports as project-sensitive and redact them before sending outside the team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-flag-janitor)
- [Canlah AI homepage](https://canlah.ai)
- [Publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with code snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-file analysis; no external API behavior reported by evidence.]

## Skill Version(s):

1.0.3 (source: server evidence release.version, skill metadata, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
