## Description: <br>
Genderize (genderize.io) helps an agent query Genderize through an OOMOL-connected account for gender prediction requests instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect the live OOMOL Genderize connector schema and run read-only single-name or batch gender prediction actions through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL account connection for Genderize and uses credentials injected by OOMOL server-side. <br>
Mitigation: Only run the OOMOL login, connection, or CLI installation flow when the user trusts the integration and an action fails because setup is missing. <br>
Risk: Genderize requests through OOMOL may consume account credits. <br>
Mitigation: Treat billing or insufficient-credit errors as a stop condition and ask the user to resolve billing before retrying. <br>


## Reference(s): <br>
- [Genderize ClawHub Skill](https://clawhub.ai/oomol/oo-genderize) <br>
- [Genderize Homepage](https://genderize.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect the live connector schema before constructing payloads and returns Genderize connector responses as JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
