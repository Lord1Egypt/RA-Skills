## Description:

Daily Precision Picker screens Chinese A-share stock candidates through a four-layer funnel using moving-average support, fundamental risk checks, fund-flow scoring, sector signals, and volume-price quality to produce tiered stock watchlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyanjun](https://clawhub.ai/user/xiyanjun)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent operators use this skill to turn a stock candidate pool into a daily tiered screening report and optional structured JSON output. The skill is designed for signal review and monitoring, not automated investment execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted stock-code input can reach shell command execution in the helper script.

Mitigation: Validate stock codes against expected market-code patterns and invoke subprocesses with shell-free argument lists before installation.

Risk: The helper script installs and runs an npm package dynamically during finance and fund-flow checks.

Mitigation: Review or pin the dependency with integrity controls before use.

Risk: The optional JSON path can write screening results to a user-supplied location.

Mitigation: Restrict JSON output paths to an approved workspace or reporting directory.

## Reference(s):

- [Research Findings](artifact/references/research_findings.md)
- [ClawHub Skill Page](https://clawhub.ai/xiyanjun/skills/hectorlee-daily-precision-picker)
- [Publisher Profile](https://clawhub.ai/user/xiyanjun)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Terminal report with tiered tables, optional JSON file, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include data availability status and a finance disclaimer; JSON output contains tier1, tier2, tier3, and availability fields.]

## Skill Version(s):

2.2.1 (source: server evidence, manifest.yaml, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
