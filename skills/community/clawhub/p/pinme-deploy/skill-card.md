## Description:

PinMe Deploy helps agents deploy static frontend sites to IPFS through Pinata by identifying project type, building when needed, uploading the output, and returning access URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish static HTML and frontend projects to IPFS for preview, sharing, or static hosting. It supports project detection, optional build steps, Pinata upload commands, and access URL generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run project build commands such as npm install or npm run build.

Mitigation: Use it only on trusted projects and inspect package.json scripts before allowing build commands.

Risk: Uploaded files may become public and difficult to remove from IPFS gateways.

Mitigation: Review build output before upload and avoid publishing secrets, private files, or unreleased content.

Risk: The skill requires Pinata API credentials.

Mitigation: Use scoped Pinata credentials with the minimum permissions needed for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/skills/pinme-deploy)
- [IPFS documentation](https://ipfs.io/)
- [Pinata documentation](https://docs.pinata.cloud/)
- [Web3.storage](https://web3.storage/)
- [Fleek](https://fleek.co/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, environment variable guidance, and deployment URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PINATA_API_KEY, PINATA_SECRET_KEY, and curl; may run npm install or npm run build before uploading files to IPFS.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
