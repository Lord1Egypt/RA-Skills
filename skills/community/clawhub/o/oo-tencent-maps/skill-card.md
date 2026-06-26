## Description: <br>
Tencent Maps helps agents search and read Tencent Maps data through OOMOL's oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to geocode addresses, search places, plan routes, query weather, and retrieve Tencent Maps data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, coordinates, IP addresses, routes, and weather locations may be sent through OOMOL and Tencent Maps. <br>
Mitigation: Use the skill only for intended Tencent Maps tasks and avoid sensitive location data unless the user approves and account policies allow it. <br>
Risk: The skill depends on an installed and authenticated oo CLI with a connected Tencent Maps account. <br>
Mitigation: Run setup steps only after an authentication or connection failure, and have the user handle login, account connection, and billing issues. <br>
Risk: If the oo CLI is missing, setup may involve remote installation scripts. <br>
Mitigation: Review OOMOL installation instructions and script source before running installation commands in a user environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-tencent-maps) <br>
- [Tencent Maps Homepage](https://lbs.qq.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Tencent Maps Connection Setup](https://console.oomol.com/app-connections?provider=tencent_maps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; oo CLI action responses are JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
