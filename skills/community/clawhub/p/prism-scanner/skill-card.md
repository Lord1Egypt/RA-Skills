## Description: <br>
Instant rug pull detection for any token. Holder concentration, liquidity locks, contract risks. DYOR before you ape. Works with AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, token analysts, and agent operators use this skill to request token risk scans and summarize PRISM API findings for rug-pull, copycat, liquidity, holder concentration, and contract-risk checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token symbols or contract addresses are sent to the configured PRISM API during scans. <br>
Mitigation: Install and run the skill only where sending those identifiers to the PRISM API is acceptable. <br>
Risk: Scan results can be incomplete or mistaken and should not be treated as financial advice or a complete audit. <br>
Mitigation: Use scan output as one risk signal and require independent review before making token, trading, or deployment decisions. <br>
Risk: The shell script depends on curl and jq being available in the runtime environment. <br>
Mitigation: Confirm both dependencies are installed before relying on the scanner in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/NextFrontierBuilds/prism-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/NextFrontierBuilds) <br>
- [PRISM API base URL](https://strykr-prism.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON scan summaries with shell usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; can use PRISM_URL and optional PRISM_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
