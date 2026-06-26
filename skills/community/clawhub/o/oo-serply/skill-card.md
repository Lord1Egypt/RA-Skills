## Description: <br>
Serply enables an agent to search Google web, news, video, and Scholar results through the OOMOL oo CLI and a connected Serply account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Serply-backed search actions from an agent after connecting their OOMOL account. It is suited for web, news, video, and academic search workflows that need JSON results and execution metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and connector activity may be processed through OOMOL and Serply. <br>
Mitigation: Confirm the user trusts OOMOL and Serply with the submitted queries before installing or using the connector. <br>
Risk: Installer, login, or connection flows can change local setup or account state if run unnecessarily. <br>
Mitigation: Run setup commands only after a command fails with a matching CLI, authentication, connection, scope, credential, or billing error. <br>
Risk: Connector action payloads may become invalid if the live contract changes. <br>
Mitigation: Inspect the live action schema before constructing each action payload. <br>


## Reference(s): <br>
- [Serply homepage](https://serply.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Serply on ClawHub](https://clawhub.ai/oomol/oo-serply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and execution metadata when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
