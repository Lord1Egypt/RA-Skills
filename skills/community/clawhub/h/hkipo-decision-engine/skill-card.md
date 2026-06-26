## Description: <br>
Score Hong Kong IPOs, build decision cards, and batch-evaluate symbols or watchlists with explainable factors and execution guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate Hong Kong IPO participation decisions, position sizing, and batch watchlist decisions with explainable factors and execution guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores IPO preferences, watchlists, parameter versions, suggestions, and review history under ~/.hkipo-next. <br>
Mitigation: Avoid entering unnecessary personal financial details, review stored local files, and delete local data when it is no longer needed. <br>
Risk: Queried IPO symbols may be sent to external market-data sites. <br>
Mitigation: Use only symbols you are comfortable disclosing to those sources and review network access expectations before running the CLI. <br>
Risk: IPO scores and decision cards can be incomplete, stale, or unsuitable for a user's financial circumstances. <br>
Mitigation: Independently verify market data and consult appropriate investment, broker, tax, and compliance guidance before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackstoic/hkipo-decision-engine) <br>
- [Publisher profile](https://clawhub.ai/user/hackstoic) <br>
- [hkipo-next README](runtime/hkipo-next/README.md) <br>
- [AiPO API reference](runtime/hkipo-next/references/aipo-api.md) <br>
- [Analysis guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [API guide](runtime/hkipo-next/references/api-guide.md) <br>
- [IPO mechanism guide](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Risk preferences guide](runtime/hkipo-next/references/risk-preferences.md) <br>
- [AiPO data source](https://aipo.myiqdii.com) <br>
- [AAStocks IPO market page](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, text, or Markdown CLI output with shell-command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist review records, profile data, watchlists, parameters, and suggestions under ~/.hkipo-next.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
