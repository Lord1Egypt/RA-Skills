## Description:

Learn how to claim pixels on MillionFinneyHomepage, a 1000x1000 on-chain pixel grid. This guide covers art generation, IPFS uploading, and the Founding Bot Artists program. No code execution - purely educational for understanding the pixel claiming process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l0c0luke](https://clawhub.ai/user/l0c0luke)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to understand how MillionFinneyHomepage pixel planning, image-to-pixel conversion, IPFS media attachment, and Ethereum contract interactions work before taking any on-chain action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes blockchain transaction guidance that can spend ETH and create permanent on-chain records.

Mitigation: Require explicit human approval before signing messages, submitting transactions, purchasing pixels, setting media, or interacting with auctions.

Risk: Wallet private keys, API keys, signed messages, and media upload credentials could be exposed or misused.

Mitigation: Keep secrets out of prompts and shared files, use a dedicated wallet with limited funds, and review any generated code or shell command before execution.

Risk: Pixel media and NFT metadata may be immutable after contract submission.

Mitigation: Preview artwork, verify token IDs and IPFS URIs, test on a testnet or dry run where possible, and start with a small purchase.

## Reference(s):

- [Millionfinney Homepage skill page](https://clawhub.ai/l0c0luke/skills/millionfinney-homepage)
- [Million Finney Homepage Contract Reference](references/contract.md)
- [Pixel Pattern & Artwork Recipes](references/pixel-art.md)
- [Million Finney Homepage IPFS upload API](https://millionfinneyhomepage.com/api/ipfs/upload)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code examples and optional JSON or CSV pixel payload files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can convert raster images into pixel payload rows with coordinates, token IDs, colors, and titles.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
