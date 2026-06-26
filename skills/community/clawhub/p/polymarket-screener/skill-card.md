## Description: <br>
Filter Polymarket prediction markets and track probabilities. Use when screening bets, drafting analyses, outlining trends, tracking price movements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to screen public Polymarket prediction markets, inspect odds and liquidity, track market movements, and draft market-analysis outputs. It supports analysis only and does not place bets or manage positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package contains an unrelated content-writing helper that silently logs user inputs locally. <br>
Mitigation: Use only scripts/polymarket.sh for Polymarket API reading, and do not enter sensitive strategy notes or private analysis into the unrelated helper. <br>
Risk: Scripts write local cache or history files under user data directories. <br>
Mitigation: Review generated files under ~/.polymarket-screener and the configured XDG data directory, and run in a disposable environment when testing. <br>
Risk: Prediction-market analysis can be mistaken for financial advice or automated trading support. <br>
Mitigation: Treat outputs as analysis only, verify market data and resolution criteria independently, and make any trading decisions outside the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/polymarket-screener) <br>
- [Publisher Profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples and market-analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local cache and history files when scripts are run.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
