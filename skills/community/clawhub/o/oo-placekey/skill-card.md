## Description: <br>
Placekey helps agents resolve postal addresses, geocodes, and Placekey identifiers through OOMOL-connected Placekey actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up Placekey identifiers, resolve addresses into geocoded responses, and run bulk Placekey lookups through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address and location data is sent through OOMOL as the intermediary for Placekey requests. <br>
Mitigation: Install and use the skill only when that data path is acceptable for the user's task and organization. <br>
Risk: The skill requires connected Placekey credentials through OOMOL. <br>
Mitigation: Use an OOMOL-connected account with appropriate Placekey access and avoid exposing raw API credentials in prompts or shell commands. <br>
Risk: First-time setup may involve running an external oo CLI installer. <br>
Mitigation: Review the oo CLI installer before running optional setup commands, and run setup only when the connector command fails for an installation or authentication reason. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-placekey) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Placekey Homepage](https://www.placekey.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing payloads; bulk lookup supports up to 100 locations per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
