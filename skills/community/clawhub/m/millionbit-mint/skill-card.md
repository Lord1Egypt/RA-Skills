## Description: <br>
Mint an image as an NFT plot on the Million Bit Homepage, a permanent 1024x1024 pixel canvas on the Base blockchain, with image resizing, availability checks, price queries, pixel encoding, and transaction preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[millionbithomepage](https://clawhub.ai/user/millionbithomepage) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare Million Bit Homepage NFT plot mints on Base, including choosing grid-aligned coordinates, checking price and availability, encoding image data, and producing transaction JSON for an EVM wallet skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted image filename could cause unintended local JavaScript execution during mint preparation. <br>
Mitigation: Use only trusted, plainly named local image files and review the skill before installing or running mint preparation. <br>
Risk: A submitted mint spends real ETH plus gas and publishes the image, URL, and metadata on Base in a way that is effectively irreversible. <br>
Mitigation: Inspect the prepared transaction fields, price, target contract, chainId, coordinates, URL, and image content before approving the transaction in an EVM wallet skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/millionbithomepage/millionbit-mint) <br>
- [Publisher profile](https://clawhub.ai/user/millionbithomepage) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [JSON transaction objects and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prepared mint transactions target Base chainId 8453 and require separate wallet review and submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
