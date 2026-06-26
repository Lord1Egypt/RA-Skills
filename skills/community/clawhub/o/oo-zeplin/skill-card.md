## Description: <br>
Provides agent access to Zeplin data through the OOMOL oo CLI for reading user, project, design-token, and screen-version information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a connected OOMOL and Zeplin account use this skill to inspect Zeplin user, project, design-token, and screen-version data from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup documentation includes remote installer commands that can execute shell code. <br>
Mitigation: Do not let an agent run the curl or PowerShell installer automatically; use the official install guide and inspect or verify the installer before execution. <br>
Risk: Commands operate through a connected OOMOL account and may access Zeplin workspace data. <br>
Mitigation: Run only the requested read action, inspect the live connector schema before building payloads, and confirm any future account-changing action with the user before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-zeplin) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Zeplin homepage](https://zeplin.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo connector schema and run commands; connector responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
