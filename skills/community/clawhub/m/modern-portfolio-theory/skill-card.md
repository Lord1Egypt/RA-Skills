## Description:

Modern Portfolio Theory optimizer - build, backtest, and manage diversified portfolios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interactively create portfolio configurations, run a local Python CLI for Modern Portfolio Theory optimization and backtesting, and interpret results in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A portfolio delete command could remove folders outside the intended portfolio area if used with an untrusted or path-like portfolio name.

Mitigation: Run the skill as an unprivileged user in an isolated virtual environment; avoid delete with untrusted names and verify the resolved directory before using --force.

Risk: Email notification settings can expose SMTP secrets if credentials are stored directly in configuration files.

Mitigation: Store SMTP credentials in environment variables and reference them from configuration.

Risk: Cron entries can continue running portfolio checks after interactive setup is complete.

Mitigation: Install only cron entries that the user understands and can later inspect, modify, or remove.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joeyiptk/skills/modern-portfolio-theory)
- [Deployment: OpenClaw Skill](docs/deployment-openclaw.md)
- [README](README.md)
- [Setup: Modern Portfolio Theory Optimizer](SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration edits, and plain-language analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create or update portfolio config files and run local CLI commands that generate reports under the portfolio directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
