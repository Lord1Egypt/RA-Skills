## Description: <br>
Beaconcha.in helps agents use the Beaconcha.in connector through the OOMOL oo CLI for read-only Ethereum validator and network lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to retrieve Beaconcha.in network performance, staking queue, validator snapshot, and finalized-epoch consensus reward data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Beaconcha.in account and sends lookup inputs such as validator identifiers, chain names, and epochs through the connector. <br>
Mitigation: Use only intended lookup inputs, confirm the connected account is appropriate for the task, and avoid submitting unnecessary sensitive data. <br>
Risk: First-time setup may require installing the oo CLI before the skill can run connector commands. <br>
Mitigation: Review the installer source before running the one-time setup command, as recommended by the security guidance. <br>
Risk: Incorrect action payloads can produce failed or misleading lookup results if they do not match the live connector schema. <br>
Mitigation: Inspect the action schema with oo connector schema before constructing command payloads. <br>


## Reference(s): <br>
- [Beaconcha.in homepage](https://beaconcha.in) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-beaconchain) <br>


## Skill Output: <br>
**Output Type(s):** [Text guidance, Markdown, Shell commands, Configuration guidance, JSON API responses] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions are intended for read-only Beaconcha.in lookups; command responses can be returned as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
