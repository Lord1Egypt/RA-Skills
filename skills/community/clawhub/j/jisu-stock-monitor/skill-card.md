## Description:

Checks stock holdings once for profit and loss, intraday moves, gaps, moving averages, RSI, trailing take-profit signals, and alert cooldowns using JisuAPI market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a one-time health check on configured stock holdings and summarize triggered alert rules. It helps report market-data indicators and configured threshold events without presenting the result as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JisuAPI key and sends stock codes to JisuAPI.

Mitigation: Use a dedicated API key and install the skill only when sharing those stock codes with JisuAPI is acceptable.

Risk: The optional state file can overwrite any writable path supplied in the config.

Mitigation: Use only trusted configs and set `state_file` to a dedicated state path.

Risk: Configs and state files may contain local holding and cost data.

Mitigation: Keep local config and state files out of public repositories and avoid running configs from others.

Risk: The skill depends on local Python package installation.

Mitigation: Install dependencies in a virtual environment with pinned versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/jisu-stock-monitor)
- [JisuAPI Stock Query API](https://www.jisuapi.com/api/stock/)
- [JisuAPI Stock History API](https://www.jisuapi.com/api/stockhistory/)
- [JisuAPI Website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON results with optional Markdown summaries, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JISU_API_KEY environment variable and may read or write a configured local state file.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
