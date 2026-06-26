## Description: <br>
AMap helps an agent use the OOMOL AMap connector for geocoding, place search, routing, IP location, weather, and district lookup through the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to retrieve AMap place, address, route, weather, IP location, and administrative district information through an authenticated OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, coordinates, route requests, IP lookup inputs, weather searches, and place searches may be processed by the OOMOL or AMap connector. <br>
Mitigation: Avoid sending sensitive location data unless the user intends to use the connected AMap service for that request. <br>
Risk: First-time setup can include a remote oo CLI installer command when the CLI is missing. <br>
Mitigation: Prefer a verified OOMOL installation path or review OOMOL's official install instructions before running the remote installer. <br>
Risk: The skill depends on an authenticated OOMOL account and connected AMap credentials. <br>
Mitigation: Use setup steps only after an auth or connection failure, and do not proactively start login or connection flows. <br>


## Reference(s): <br>
- [ClawHub AMap skill page](https://clawhub.ai/oomol/oo-amap) <br>
- [AMap homepage](https://www.amap.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payload examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit JSON returned by the oo connector when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
