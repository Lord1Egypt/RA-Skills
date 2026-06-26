## Description: <br>
PinMe Deploy helps agents build and publish frontend static sites to IPFS through Pinata, returning accessible deployment URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to detect, build, and deploy static frontend projects such as HTML, React, Vue, and static asset sites to IPFS. It is intended for quick previews, sharing, and static-site hosting workflows that use Pinata credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploads to IPFS through Pinata may publish selected site output publicly and persistently. <br>
Mitigation: Inspect the build directory before deployment and remove secrets, private source, internal assets, or unintended files. <br>
Risk: The workflow uses sensitive Pinata API credentials. <br>
Mitigation: Keep PINATA_API_KEY and PINATA_SECRET_KEY out of logs and shared terminals, and rotate keys if exposed. <br>
Risk: Build commands such as npm install and npm run build execute project code. <br>
Mitigation: Run build steps only for trusted projects or inside a sandboxed environment. <br>


## Reference(s): <br>
- [PinMe Deploy on ClawHub](https://clawhub.ai/yz6214589-hash/pinme-deploy) <br>
- [IPFS](https://ipfs.io/) <br>
- [Pinata Documentation](https://docs.pinata.cloud/) <br>
- [Web3.storage](https://web3.storage/) <br>
- [Fleek](https://fleek.co/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps and IPFS gateway URLs; requires Pinata API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
