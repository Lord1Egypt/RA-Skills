## Description: <br>
Interactive Brokers (IBKR) trading automation via the Client Portal API for account access, session authentication, portfolio and position checks, trading bot workflows, and IBeam login with IBKR Key 2FA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlokieW](https://clawhub.ai/user/FlokieW) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and trading-system operators use this skill to configure IBKR Client Portal access, authenticate sessions with IBeam and IBKR Key, inspect account data, and build trading automation against the IBKR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give automation high-impact trading authority without enough safety controls. <br>
Mitigation: Use an IBKR paper account first, and add explicit human approval, account limits, symbol allowlists, and maximum order-size controls before connecting to a live brokerage account. <br>
Risk: Credential material may be stored in a plaintext .env file. <br>
Mitigation: Protect or avoid the plaintext .env credential file and restrict access to the trading environment. <br>
Risk: Cron keepalive and automatic re-authentication can extend trading-session availability. <br>
Mitigation: Disable cron keepalive unless it is required, and require phone approval and operational monitoring for re-authentication. <br>
Risk: The setup downloads the IBKR gateway and installs Python dependencies before use. <br>
Mitigation: Verify the IBKR gateway download and Python dependencies before installation. <br>


## Reference(s): <br>
- [IBKR Client Portal API Reference](artifact/references/api-endpoints.md) <br>
- [IBKR Client Portal Gateway Download](https://download2.interactivebrokers.com/portal/clientportal.gw.zip) <br>
- [ClawHub Skill Page](https://clawhub.ai/FlokieW/ibkr-trader) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/FlokieW) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, Python code, and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, API usage examples, session-management guidance, and starter automation scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
