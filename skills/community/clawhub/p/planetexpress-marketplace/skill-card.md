## Description: <br>
Decentralized file marketplace on Monad blockchain - buy, sell, and browse encrypted files with x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timowhite88](https://clawhub.ai/user/timowhite88) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can use this skill to browse encrypted file listings, purchase files through x402 payment flows, and list files for sale on the Planet Express marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace purchase and listing flows can involve real payments and irreversible on-chain actions. <br>
Mitigation: Before any payment or listing, manually confirm the exact cost, chain, contract or recipient, wallet prompt, and listing details. <br>
Risk: Public listings can expose file titles, descriptions, URIs, prices, and related marketplace metadata. <br>
Mitigation: Review the file and listing metadata before publishing, and avoid listing sensitive material unless public exposure is intended. <br>
Risk: The skill depends on external marketplace and payment endpoints for browsing, purchasing, listing, and delivery. <br>
Mitigation: Use the documented Planet Express and DropClaw endpoints, verify listing identity and payment options, and stop if endpoint, contract, or wallet details do not match expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timowhite88/planetexpress-marketplace) <br>
- [Planet Express marketplace](https://planetexpress.dropclaw.cloud) <br>
- [DropClaw marketplace API](https://dropclaw.cloud/marketplace) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/claw.json](artifact/claw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with HTTP request examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network-enabled marketplace guidance involving x402 payment flows, encrypted file listings, and chain-specific payment details.] <br>

## Skill Version(s): <br>
2.0.0 (source: artifact/claw.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
