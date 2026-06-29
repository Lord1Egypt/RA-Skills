## Description: <br>
BlazeMeter Performance helps an agent inspect live BlazeMeter user, account, workspace, project, test, and test-detail data through the OOMOL `blaze_meter_performance` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and QA teams use this skill to let an agent query BlazeMeter Performance resources from an already connected OOMOL account. It supports read-only discovery of user profiles, accounts, workspaces, projects, tests, and individual test details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger wording is broad and may route ambiguous BlazeMeter-related requests to this skill. <br>
Mitigation: Clarify ambiguous BlazeMeter requests before invoking the skill or running connector actions. <br>
Risk: Future versions could add write or destructive BlazeMeter actions. <br>
Mitigation: Review future releases before deployment and require explicit user confirmation for any write or destructive action. <br>
Risk: The skill relies on live OOMOL and BlazeMeter account connectivity, so auth, connection, scope, or billing issues can block execution. <br>
Mitigation: Use the documented first-time setup and troubleshooting paths only after a connector command fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-blaze-meter-performance) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [BlazeMeter Performance homepage](https://www.blazemeter.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON with `data` and `meta.executionId` fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
