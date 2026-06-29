## Description: <br>
GitLab (gitlab.com) skill for reading, creating, and updating GitLab data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to inspect GitLab user, project, and issue data and to create project issues through their connected OOMOL GitLab account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected GitLab account and can access GitLab data through that connection. <br>
Mitigation: Confirm the connected account and OOMOL CLI trust boundary before use, and review returned data according to the user's access expectations. <br>
Risk: Issue creation changes GitLab project state. <br>
Mitigation: Fetch the live connector schema, show the exact payload and intended effect, and get explicit user confirmation before running write actions. <br>
Risk: First-time setup may require running an external OOMOL CLI installation command. <br>
Mitigation: Run installation only when the CLI is missing and only after the user confirms they trust the OOMOL CLI source. <br>


## Reference(s): <br>
- [GitLab](https://gitlab.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution; write actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
