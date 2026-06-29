## Description: <br>
Provides read-oriented Laravel Cloud operations through the OOMOL laravel_cloud connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Laravel Cloud applications, environments, deployments, regions, and organization details from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Laravel Cloud data through an OOMOL-connected account. <br>
Mitigation: Install it only when the agent should read Laravel Cloud data, and review the OOMOL connection and API key scopes before use. <br>
Risk: Future connector actions labeled write or destructive could change or remove Laravel Cloud data. <br>
Mitigation: Require explicit user confirmation of the exact payload and expected effect before running any write or destructive action. <br>
Risk: Initial setup may require installing the oo CLI and connecting Laravel Cloud credentials. <br>
Mitigation: Run setup only after an authentication or connection failure, and keep credentials managed through OOMOL rather than exposing raw tokens to the agent. <br>


## Reference(s): <br>
- [ClawHub Laravel Cloud skill page](https://clawhub.ai/oomol/skills/oo-laravel-cloud) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Laravel Cloud homepage](https://cloud.laravel.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live oo connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
