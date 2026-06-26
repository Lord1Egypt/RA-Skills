## Description: <br>
This skill helps agents search and read Tripadvisor data through the OOMOL Tripadvisor connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Tripadvisor locations, retrieve location details, and fetch location photos through an OOMOL-connected Tripadvisor account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and Tripadvisor credentials managed through OOMOL. <br>
Mitigation: Install and use it only when OOMOL is an acceptable operator for the connected Tripadvisor account. <br>
Risk: The first-time setup path includes optional curl-to-shell and PowerShell installer commands for the oo CLI. <br>
Mitigation: Prefer the official oo CLI installation guide or inspect and verify installer scripts before running them. <br>
Risk: Future connector actions could include create, update, or delete behavior. <br>
Mitigation: Require explicit user approval before running any action marked write or destructive, including the exact payload and intended effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-tripadvisor) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Tripadvisor developer homepage](https://www.tripadvisor.com/developers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects returned by the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
