## Description:

Uses SellerSprite market-research data to screen Amazon category markets by market size, competition, concentration, seller structure, new-product share, pricing, ratings, and margin filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, marketplace analysts, and agents use this skill to evaluate Amazon category opportunities and shortlist markets with SellerSprite metrics. It can also guide LinkFox authentication, billing, and API-key setup when access or balance errors block use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-research inputs and session metadata are sent to LinkFox/SellerSprite services.

Mitigation: Install and use the skill only when those data flows are acceptable, and avoid sending sensitive or unnecessary business information in requests.

Risk: Onboarding can handle SMS login codes, API keys, billing orders, and payment QR codes.

Mitigation: Paste SMS codes only when intentionally linking the account, confirm any order before payment, and store API keys in a secret manager rather than shell startup files or logs.

Risk: Full market-research responses are written to local LinkFox session directories.

Mitigation: Review output locations before use, limit sensitive query content, and clean up saved response files according to the user's retention requirements.

Risk: Endpoint override environment variables can redirect requests away from the default LinkFox services.

Mitigation: Use default endpoints unless an administrator has reviewed and approved the override values.

## Reference(s):

- [SellerSprite Market Research API Reference](artifact/references/api.md)
- [LinkFox Authentication and Billing Onboarding](artifact/references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-sellersprite-market-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, and local JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full market-research responses are saved under a LinkFox session data directory; large responses are summarized on stdout, and repeated parameter combinations may use a 24-hour local cache.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
