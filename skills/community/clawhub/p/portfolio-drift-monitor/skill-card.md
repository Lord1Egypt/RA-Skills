## Description: <br>
Monitors Kalshi portfolio positions and reports drift alerts when holdings, price, or P&L changes exceed a configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agents use this skill to monitor Kalshi positions, compare current portfolio state against a local snapshot, and surface drift alerts between scheduled portfolio reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack webhook delivery can send portfolio details outside the local environment when OPENCLAW_SLACK_WEBHOOK or slack_webhook_url is configured. <br>
Mitigation: Configure Slack delivery only when intentional, use a trusted destination, and avoid exposing webhook URLs or sensitive portfolio data. <br>
Risk: The skill requires Kalshi API credentials and stores a local portfolio snapshot. <br>
Mitigation: Use the least-privileged Kalshi API key available and protect both the private key file and ~/.openclaw/state/portfolio_snapshot.json with appropriate local permissions. <br>
Risk: The artifact includes an agent bug-fix protocol that asks agents to edit files and commit changes. <br>
Mitigation: Treat those instructions as artifact behavior only and authorize code edits or commits separately before allowing an agent to modify installed skill files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kingmadellc/portfolio-drift-monitor) <br>
- [Portfolio Drift Monitor Configuration Reference](references/drift-config.md) <br>
- [Kalshi API Documentation](https://docs.kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text alerts and Markdown documentation with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local snapshot state and optional Slack delivery when configured.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
