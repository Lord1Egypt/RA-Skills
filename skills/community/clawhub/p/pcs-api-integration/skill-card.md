## Description: <br>
Help apps and distribution channels integrate PCS Hub into their frontend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to design quote, route, and execution handoff flows for embedding PCS Hub swap functionality in wallets, mobile apps, webviews, partner browsers, or headless bots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an under-disclosed background ping that sends basic agent and system details to pancakeswap.ai before the requested work. <br>
Mitigation: Review or remove the initialization step before installing or invoking the skill if you do not want the agent to contact pancakeswap.ai with those details. <br>
Risk: The skill can use a PCS Hub API token while generating integration guidance. <br>
Mitigation: Keep the token scoped, read it from the environment, and confirm the agent sends it only to the intended PancakeSwap Hub API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcs-bot/pcs-api-integration) <br>
- [PancakeSwap AI homepage](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [PCS Hub API base](https://hub-api.pancakeswap.com/aggregator) <br>
- [PancakeSwap token list](https://tokens.pancakeswap.finance/pancakeswap-extended.json) <br>
- [BNB Chain public RPC](https://bsc-dataseed1.binance.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API contract examples and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration specifications and implementation guidance, not executable swap code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
