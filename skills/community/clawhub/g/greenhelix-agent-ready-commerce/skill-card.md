## Description: <br>
Guides developers and commerce teams in building agent-discoverable storefronts, API-first product feeds, payment flows, and marketplace integrations for AI shopping agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, commerce platform teams, and merchants use this guide to retrofit product catalogs, storefront manifests, API endpoints, and checkout flows for AI shopping agents. It focuses on structured product data, GreenHelix marketplace registration, UCP/ACP/x402 payment patterns, escrow, subscriptions, and agent discoverability testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide references sensitive payment, wallet, and signing credentials. <br>
Mitigation: Use sandbox or test credentials, keep secrets out of source code, and avoid providing production Stripe keys, signing keys, or funded wallet access just to read or evaluate the guide. <br>
Risk: Copied payment examples can move or automatically release funds if run against live services. <br>
Mitigation: Add explicit approval steps, spending caps, and test wallets before running payment, escrow, subscription, or deposit examples. <br>
Risk: Automatic top-up, subscription, or escrow-release patterns can create unintended financial actions in production. <br>
Mitigation: Review and gate these flows before production use, with least-privilege credentials and operational monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/greenhelix-agent-ready-commerce) <br>
- [GreenHelix Sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API Endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with code examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable educational guide; examples reference sensitive commerce credentials and payment flows.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
