## Description: <br>
An autonomous trading agent for Polymarket (Polygon) that scans 15-minute markets for momentum, supports simulation mode, and can execute live trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjs829](https://clawhub.ai/user/wjs829) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to deploy and operate a Polymarket momentum-trading agent with a Flask dashboard, SQLite persistence, OpenClaw scheduling, simulation mode, and optional live order execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate as a real-money autonomous trading bot with wallet and Polymarket API authority. <br>
Mitigation: Run in simulation first, use a burner wallet with limited funds, set explicit spend limits, and define a stop procedure before enabling scheduled live scans. <br>
Risk: Private keys and API credentials may be placed in local configuration files. <br>
Mitigation: Avoid plaintext secrets where possible, restrict file permissions, use scoped API keys, and keep private keys out of shared workspaces and logs. <br>
Risk: The dashboard binds to 0.0.0.0 on port 5000 and could expose trading state if reachable publicly. <br>
Mitigation: Restrict access with firewall rules or a private network and do not expose the dashboard directly to the public internet. <br>
Risk: The bootstrap flow installs dependencies and the trading logic includes fallback pricing and demo momentum behavior. <br>
Mitigation: Review the code before installation, pin dependencies in a virtual environment, and remove or gate fallback trading behavior before live use. <br>
Risk: License validation defaults to a local HTTP endpoint when configured for pro mode. <br>
Mitigation: Verify that any license server used for live operation is trusted and served over HTTPS. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wjs829/polymarket-sniper-bot-standalone) <br>
- [Project Website from Metadata](https://github.com/wjs829/polymarket-sniper-skill) <br>
- [Polymarket Gamma API Endpoint](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API Endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with Python, YAML, shell commands, and dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance and local automation artifacts for a trading agent; live operation depends on user-supplied wallet, RPC, and Polymarket API credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
