## Description: <br>
Enables agents to read SatisMeter projects, surveys, survey statistics, and responses through the OOMOL-connected oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and external agents use this skill to inspect SatisMeter customer feedback data without handling raw API tokens. It supports read-only project, survey, survey statistics, and response retrieval through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected SatisMeter credentials and can return customer feedback data. <br>
Mitigation: Use it only with accounts authorized to access the relevant SatisMeter projects and review returned data before sharing it. <br>
Risk: Connector payloads can become invalid if the live SatisMeter action schema changes. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>
Risk: Setup and recovery commands can initiate authentication, connection, or billing workflows. <br>
Mitigation: Run setup, reconnection, or billing steps only after a command fails with the matching error. <br>


## Reference(s): <br>
- [SatisMeter homepage](https://satismeter.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub SatisMeter skill page](https://clawhub.ai/oomol/oo-satismeter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only SatisMeter connector actions; requires the oo CLI, an OOMOL account, and connected SatisMeter credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
