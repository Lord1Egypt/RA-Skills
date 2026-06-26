## Description: <br>
Guides agents through P2P energy trading patterns for prosumer microgrids, including prosumer registration, smart meter integration, dynamic pricing, escrow-protected settlement, multi-agent orchestration, and regulatory compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and energy platform builders use this guide to design agent workflows for prosumer microgrids, including energy offers, smart meter verification, escrow settlement, EV charging coordination, and compliance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide describes autonomous energy-control and payment workflows that could affect live grid devices or payment accounts if applied without review. <br>
Mitigation: Treat examples as sandbox-only until qualified energy, payments, and compliance operators approve the design and deployment plan. <br>
Risk: Examples reference sensitive GreenHelix and Stripe credentials. <br>
Mitigation: Use least-privilege credential scopes, explicit human approvals, spending and dispatch limits, monitoring, safety interlocks, and tested rollback procedures before any live use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/greenhelix-agent-energy-p2p-trading) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guide with Python code examples and credential notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing guide; examples reference GREENHELIX_API_KEY and STRIPE_API_KEY for user-managed environments.] <br>

## Skill Version(s): <br>
1.3.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
