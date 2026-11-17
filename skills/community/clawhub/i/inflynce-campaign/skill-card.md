## Description:

Create and launch Inflynce Boost campaigns to promote any HTTPS link by paying USDC rewards to real users on Base based on social influence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inflynceprotocol](https://clawhub.ai/user/inflynceprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, creators, and developers use this skill to create Inflynce Boost campaigns for tweets, websites, Farcaster casts, and other HTTPS links. The skill supports campaign creation, payment proof submission, and optional USDC fee or top-up transactions on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can broadcast real Base mainnet USDC transfer or approval transactions when supplied with a private key.

Mitigation: Prefer the Inflynce web UI or an external wallet for payments and top-ups; if programmatic signing is required, use a dedicated low-balance wallet.

Risk: Passing a wallet private key through command-line flags can expose the key through shell history or process inspection.

Mitigation: Avoid --private-key for real wallets and use environment handling or a wallet workflow that does not disclose the key to the agent.

Risk: The dependency lockfile includes a flagged transitive ws version according to the authoritative security evidence.

Mitigation: Review dependency updates before installation or deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/inflynceprotocol/skills/inflynce-campaign)
- [Inflynce Boost](https://boost.inflynce.com)
- [Inflynce GraphQL API Endpoint](https://boost.inflynce.com/api/graphql)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign creation returns a boost id, status, and creator wallet when the Inflynce API accepts the request.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
