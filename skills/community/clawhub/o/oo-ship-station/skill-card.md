## Description: <br>
ShipStation helps agents read, create, and update ShipStation data through OOMOL's ship_station connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run authenticated ShipStation connector actions for purchase-order retrieval and inventory or warehouse lookup through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected ShipStation account and relies on OOMOL to inject credentials server-side. <br>
Mitigation: Install only if you trust OOMOL and are comfortable connecting ShipStation through the oo CLI. <br>
Risk: Connector actions or payloads may affect ShipStation data, and the description is broader than the listed read-oriented actions. <br>
Mitigation: Review the proposed oo connector action, inspect the live schema, and confirm the exact payload before approving write or destructive operations. <br>
Risk: First-time setup may require installing the oo CLI from OOMOL-hosted install scripts. <br>
Mitigation: Use the documented OOMOL install sources and avoid repeating setup steps unless a command fails with the matching installation or authentication error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ship-station) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ShipStation homepage](https://www.shipstation.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to inspect live connector schemas before executing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
