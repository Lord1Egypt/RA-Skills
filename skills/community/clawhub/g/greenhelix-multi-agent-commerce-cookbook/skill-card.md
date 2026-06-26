## Description: <br>
A practitioner guide for adding escrow payments, marketplace discovery, reputation-gated hiring, and dispute resolution to CrewAI, LangGraph, and AutoGen multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this guide to design multi-agent workflows that can discover counterparties, manage escrow-backed payments, evaluate reputation, and handle disputes across CrewAI, LangGraph, and AutoGen systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and signing examples involve sensitive credentials and agent spending authority. <br>
Mitigation: Use sandbox or Stripe test mode first, store keys in a secrets manager, scope keys narrowly, and require human approval before production spending, subscriptions, or escrow release. <br>
Risk: Copied examples could authorize agents to make purchases or sign transactions without adequate budget controls. <br>
Mitigation: Set strict per-agent budgets, isolate wallets by agent, log transactions, and review workflows before enabling real funds. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mirni/greenhelix-multi-agent-commerce-cookbook) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guide with Python examples, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference GreenHelix, agent signing, and Stripe credentials supplied by the user.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
