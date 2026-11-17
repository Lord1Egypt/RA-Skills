## Description:

Reviews past Hong Kong IPO decisions, updates actual outcomes, exports review datasets, and accepts or rejects tuning suggestions so users can learn from completed IPO calls and improve later scoring behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to review completed Hong Kong IPO decisions, record actual outcomes and variance notes, export review datasets, and apply or reject scoring suggestions for future decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI can do more than the review workflow described by the skill.

Mitigation: Review available commands before use and run only the review and apply-suggestions actions needed for the task.

Risk: The runtime can write local review and scoring data and export review history.

Mitigation: Back up the local review database before updates and inspect exported datasets before sharing them.

Risk: Some market-data commands may contact external finance sites.

Mitigation: Run the skill only in environments where those outbound data-source requests are acceptable.

Risk: Dependencies are resolved through uv.

Mitigation: Use a locked or reviewed dependency set before running the bundled runtime.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hackstoic/skills/hkipo-review-optimizer)
- [hkipo-next README](runtime/hkipo-next/README.md)
- [AiPO API Reference](runtime/hkipo-next/references/aipo-api.md)
- [HK IPO Analysis Guide](runtime/hkipo-next/references/analysis-guide.md)
- [HK IPO Mechanism Reference](runtime/hkipo-next/references/ipo-mechanism.md)
- [Risk Preference Reference](runtime/hkipo-next/references/risk-preferences.md)
- [API Guide](runtime/hkipo-next/references/api-guide.md)
- [AiPO Data Source](https://aipo.myiqdii.com)
- [AAStocks IPO Data Source](https://www.aastocks.com/tc/stocks/market/ipo/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON, text, or markdown CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite review database by default and can export review datasets to files.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, pyproject.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
