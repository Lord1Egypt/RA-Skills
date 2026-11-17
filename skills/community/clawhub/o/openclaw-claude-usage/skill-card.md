## Description:

Check Claude Max plan usage limits by launching Claude Code and running /usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask an agent to check authenticated Claude Max plan usage, parse Claude Code /usage output, and return current session and weekly quota metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens an authenticated Claude Code CLI and can reveal Claude usage information, including limited local cached token counts during fallback handling.

Mitigation: Use it only in trusted agent sessions and avoid sharing returned quota or cached usage details beyond the intended user context.

Risk: The expect-based flow depends on Claude Code's interactive usage screen and may fail or misparse output if the TUI changes.

Mitigation: Review returned metrics for plausibility and treat fallback data from claude auth status or local cache files as limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chunhualiao/skills/openclaw-claude-usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with usage metrics and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Claude usage metrics after stripping ANSI output; fallback data is limited when the expect-based flow is unavailable.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact skill.yml and CHANGELOG show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
