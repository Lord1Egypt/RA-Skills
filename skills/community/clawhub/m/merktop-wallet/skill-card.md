## Description: <br>
Pay for any x402-gated API or resource and receive payments from a non-custodial Merktop wallet on Base, with each payment pulled just in time from the user's wallet under a hard on-chain spend cap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiso2](https://clawhub.ai/user/luiso2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task needs a paid x402-gated API, dataset, hosted paywall, or agent-to-agent service. It also guides users through exposing their own endpoint behind a Merktop hosted paywall so other agents can pay them in USDC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The buyer key can authorize spending from a configured Merktop budget, so careless use could spend real funds within that cap. <br>
Mitigation: Set a low budget cap, pay only for resources needed by the current task, and monitor x-merktop-spent-cents after paid calls. <br>
Risk: Putting the buyer key in a URL can expose it through shared terminal logs or proxy logs. <br>
Mitigation: Prefer the x-merktop-key header form when possible so the buyer key is not embedded in request URLs. <br>
Risk: Payment or settlement failures can make refund timing uncertain. <br>
Mitigation: For 502 pay_failed responses, verify the wallet balance before assuming a refund landed. <br>


## Reference(s): <br>
- [Merktop Documentation](https://facilitator.merktop.com/docs) <br>
- [Merktop](https://merktop.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/luiso2/skills/merktop-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and HTTP outcome guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MERKTOP_BUYER_KEY; reports paid-call cost through x-merktop-spent-cents.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
