## Description: <br>
BigDataCloud (bigdatacloud.com). Use this skill for ANY BigDataCloud request - searching and reading data through the OOMOL BigDataCloud connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform BigDataCloud read-only lookup actions through an OOMOL-connected account, including IP geolocation, network and ASN details, timezone lookup, and reverse geocoding with timezone data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected BigDataCloud account and sends lookup inputs such as IP addresses or coordinates to BigDataCloud. <br>
Mitigation: Confirm the account connection and data-sharing expectations before use, especially for sensitive IP addresses or coordinates. <br>
Risk: First-time setup may require installing the oo CLI from an external installer. <br>
Mitigation: Review the installer source before running the one-time setup command when the CLI is not already installed. <br>


## Reference(s): <br>
- [BigDataCloud homepage](https://www.bigdatacloud.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-big-data-cloud) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
