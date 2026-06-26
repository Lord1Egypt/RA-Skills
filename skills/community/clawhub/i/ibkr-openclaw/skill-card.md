## Description: <br>
Connects OpenClaw to Interactive Brokers through IB Gateway Docker for live portfolio data, quotes, historical K-lines, technical analysis, and Telegram alerts in a read-only workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amuletxheart](https://clawhub.ai/user/amuletxheart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent workflow to IBKR Gateway for portfolio monitoring, market data queries, historical data retrieval, technical analysis, and alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent brokerage access may expose live account data or enable live-mode workflows if credentials and gateway settings are mishandled. <br>
Mitigation: Prefer a paper IBKR account, keep read-only API settings enabled, and avoid live mode unless the deployment has been reviewed. <br>
Risk: The setup stores IBKR credentials in a plaintext .env file. <br>
Mitigation: Do not store a main brokerage password in shared or backed-up workspaces, restrict file permissions, and protect the host running the gateway. <br>
Risk: The workflow depends on Docker and a third-party IB Gateway container. <br>
Mitigation: Install Docker and the gateway container only from reviewed or pinned sources, and keep VNC disabled unless it is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amuletxheart/ibkr-openclaw) <br>
- [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker) <br>
- [ib_async](https://github.com/ib-api-reloaded/ib_async) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and local CLI commands for connecting to an IB Gateway instance; command outputs may include account and market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
