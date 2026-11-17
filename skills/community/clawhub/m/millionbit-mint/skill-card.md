## Description:

Mint an image as an NFT plot on the Million Bit Homepage, a permanent 1024x1024 pixel canvas on the Base blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[millionbithomepage](https://clawhub.ai/user/millionbithomepage)

### License/Terms of Use:


## Use Case:

Developers, agents, and project operators use this skill to check Million Bit Homepage plot pricing and availability, resize an image, and prepare a Base-chain NFT mint transaction for wallet submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled image paths, filenames, and coordinate strings can expose local code execution risks when passed into shell and Node scripts.

Mitigation: Run the skill only with trusted local image paths and plain numeric coordinates, and do not let untrusted users supply filenames or coordinate strings.

Risk: Prepared mint transactions can spend ETH and permanently publish image and URL content on Base.

Mitigation: Before wallet submission, verify the Base chain ID, contract address, ETH value, URL, image, and permanence of the on-chain publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/millionbithomepage/skills/millionbit-mint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON transaction outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepared mint transactions include Base chain ID, contract address, ETH value, calldata, and metadata for wallet review.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
