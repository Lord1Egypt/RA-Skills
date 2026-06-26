## Description: <br>
Predict.fun skill with a PolyClaw-style CLI for markets, wallet funding, trading, positions, and hedging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walioo](https://clawhub.ai/user/walioo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to browse Predict.fun markets, inspect wallet readiness, receive funding guidance, place trades, review positions, and scan hedge opportunities through a CLI-oriented workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Predict.fun wallet, approval, withdrawal, buy, and vault bootstrap actions that may move funds. <br>
Mitigation: Start in fixture or read-only mode, use low-balance keys, and manually review every approval, withdrawal, buy, or vault bootstrap command before execution. <br>
Risk: Several modes require private keys, API keys, or vault authority credentials. <br>
Mitigation: Provide only the secrets required for the selected mode and keep signer credentials isolated from unrelated agent workflows. <br>
Risk: Vault workflows depend on the external erc-mandated-mcp executable and subprocess access. <br>
Mitigation: Verify the erc-mandated-mcp executable before vault use and review any broadcast or bootstrap action before it runs. <br>


## Reference(s): <br>
- [PredictClaw README](README.md) <br>
- [Predict.fun](https://predict.fun) <br>
- [ClawHub Predictfunclaw Release](https://clawhub.ai/walioo/predictclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, dotenv configuration snippets, and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide live Predict.fun wallet, trading, funding, position, and hedge workflows depending on the selected environment and credentials.] <br>

## Skill Version(s): <br>
0.1.34 (source: pyproject.toml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
