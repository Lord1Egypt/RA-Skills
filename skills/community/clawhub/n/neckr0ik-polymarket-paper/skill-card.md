## Description: <br>
Neckr0ik Polymarket Paper is a CLI paper-trading simulator for practicing prediction-market strategies with virtual accounts, local portfolios, leaderboards, and performance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run a local Polymarket-style paper-trading simulator, practice trades with virtual funds, inspect portfolios, and review performance metrics before risking real capital. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The simulator stores virtual account names, positions, and trade history on the local filesystem. <br>
Mitigation: Use non-sensitive account names, review files under ~/.polymarket-paper, and remove local simulator data when it is no longer needed. <br>
Risk: Documentation describes live Polymarket data and leaderboard behavior, while security evidence says to treat market data and leaderboards as demo or local data unless a real integration is documented. <br>
Mitigation: Treat results as training data only and verify the executable source before relying on market data, leaderboard output, or trading assumptions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Neckr0ik/neckr0ik-polymarket-paper) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [paper_trading.py](artifact/scripts/paper_trading.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and Python code behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI output and stores virtual account, position, and trade history under ~/.polymarket-paper.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
