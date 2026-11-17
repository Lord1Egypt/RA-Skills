## Description:

Transfer files through Payaion, set USDC per-download pricing on Base mainnet, and optionally list files on its marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jan-blockbites](https://clawhub.ai/user/jan-blockbites)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw agents and their users transfer files between agents and people, share download links, and optionally sell files through the Payaion marketplace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploading a local file or URL sends its contents to Payaion.

Mitigation: Confirm the exact file or URL and obtain approval before transferring sensitive content.

Risk: A paid marketplace listing can expose selected content and generated listing details publicly.

Mitigation: Before listing, confirm the file, price, title, description, category, tags, payout address, and whether its links may be shared publicly.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jan-blockbites/skills/payaion-transfer)
- [Payaion homepage](https://payaion.com)
- [Payaion documentation](https://payaion.com/docs)
- [Payaion API reference](https://payaion.com/openapi.yaml)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with curl commands and transfer summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include upload IDs, download links, prices, and marketplace links.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
