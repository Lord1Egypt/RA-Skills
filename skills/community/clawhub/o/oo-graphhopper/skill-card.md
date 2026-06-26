## Description: <br>
GraphHopper helps agents use an OOMOL-connected GraphHopper account for routing, geocoding, isochrones, travel matrices, and custom profile listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when an agent needs to search or read GraphHopper routing, geocoding, isochrone, matrix, or profile data through the OOMOL connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an external connector. <br>
Mitigation: Install only if you trust OOMOL and intend to use GraphHopper through its connector. <br>
Risk: Route, location, and geocoding queries may be visible to connected services. <br>
Mitigation: Avoid submitting sensitive location data unless the connected account and service usage are appropriate for that data. <br>
Risk: The one-time oo CLI installer runs local installation commands. <br>
Mitigation: Review the installer before running it and use setup steps only when the CLI, authentication, or connection is missing. <br>


## Reference(s): <br>
- [ClawHub GraphHopper Skill](https://clawhub.ai/oomol/oo-graphhopper) <br>
- [GraphHopper Homepage](https://www.graphhopper.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return GraphHopper data as JSON through the oo connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
