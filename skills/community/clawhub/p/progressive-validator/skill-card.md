## Description:

Multi-stage backtest validation framework that fails fast with short windows before committing to expensive full-period backtests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative strategy engineers use this skill to plan and track staged backtest validation, moving from smoke and stress windows to medium and full-period tests only after earlier stages pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored passed statuses can be mistaken for authoritative proof that a strategy is ready to advance.

Mitigation: Treat the local results file as a tracker only, and manually verify each backtest window, metric, and unchanged strategy code before promotion.

Risk: Suggested shell commands can be unsafe when strategy names, paths, or CLI locations contain shell metacharacters.

Mitigation: Review and edit generated commands before execution, quote paths explicitly, and avoid auto-running suggestions from untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tltby12341/skills/progressive-validator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples, JSON configuration, and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The validator can persist stage results as a local JSON file.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
