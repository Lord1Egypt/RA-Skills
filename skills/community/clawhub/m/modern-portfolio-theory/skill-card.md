## Description: <br>
Modern Portfolio Theory optimizer - build, backtest, and manage diversified portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyiptk](https://clawhub.ai/user/joeyiptk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create portfolio configuration, run local CLI commands for optimization and backtesting, and interpret portfolio reports in plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local portfolio deletion path has weak safeguards and may permanently remove more local data than intended. <br>
Mitigation: Avoid the delete command, especially with --force, until portfolio names and paths are validated and deletion requires clear confirmation. <br>
Risk: The tool writes persistent local configuration, state, cached price data, generated reports, and optional cron jobs. <br>
Mitigation: Install and run it only in a workspace where those local writes are acceptable, and review generated cron entries before enabling automation. <br>
Risk: Email notification configuration can include SMTP credentials. <br>
Mitigation: Use environment-variable placeholders for SMTP settings instead of storing plaintext passwords in configuration files. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Setup Guide](SETUP.md) <br>
- [OpenClaw Deployment Guide](docs/deployment-openclaw.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/joeyiptk/modern-portfolio-theory) <br>
- [Publisher Profile](https://clawhub.ai/user/joeyiptk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, YAML configuration edits, and plain-language explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill parses CLI JSON blocks and points users to generated local HTML reports when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, CHANGELOG.md, version.txt, and server release evidence; pyproject.toml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
