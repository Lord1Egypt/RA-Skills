## Description: <br>
Use this skill for searching and reading Ambee data from getambee.com through the OOMOL-connected oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Ambee geocoding and air-quality data from a connected OOMOL account without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may install the oo CLI and connect an Ambee API key through OOMOL. <br>
Mitigation: Use a trusted installation process, review the installer source when appropriate, and connect only the intended OOMOL and Ambee accounts. <br>
Risk: The skill requires a connected account with sensitive credentials managed outside the artifact. <br>
Mitigation: Keep credentials in the OOMOL-managed connection flow and avoid placing raw API keys in prompts, files, or shell history. <br>


## Reference(s): <br>
- [Ambee homepage](https://www.getambee.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ambee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
