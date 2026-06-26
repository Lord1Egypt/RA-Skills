## Description: <br>
Infra Wrapper logs, searches, summarizes, and exports timestamped infrastructure wrapper activity for local audit tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to record, inspect, search, and export local notes about Terragrunt, OpenTofu, Terraform, and related infrastructure wrapper operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Infrastructure commands, plan output, backend URLs, account IDs, or credentials entered into the tool may be retained in local logs and exports. <br>
Mitigation: Avoid entering secrets or sensitive infrastructure details unless local retention is intended; review and purge ~/.local/share/infra-wrapper/ before sharing or archiving exports. <br>
Risk: The release is advertised as an infrastructure helper but evidence indicates it records and exports user-provided text rather than executing Terragrunt, OpenTofu, or Terraform workflows. <br>
Mitigation: Treat the skill as a local logging and audit utility, and independently verify any infrastructure actions with the appropriate IaC tooling before relying on them. <br>


## Reference(s): <br>
- [Infra Wrapper on ClawHub](https://clawhub.ai/bytesagain1/infra-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and exported JSON, CSV, or TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local log and export files under ~/.local/share/infra-wrapper/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
