## Description: <br>
Grafana Cloud helps agents search and read organization data through an OOMOL-connected Grafana Cloud account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Grafana Cloud organization information, including billed usage, stack connectivity, stack regions, and stacks, through the OOMOL `grafana_cloud` connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes `oo` CLI connector commands in a connected Grafana Cloud account context. <br>
Mitigation: Install only when the publisher is trusted, review commands before approval, and require explicit user confirmation before any write or destructive action. <br>
Risk: Authentication, connection scope, expired credentials, or billing state can block connector execution. <br>
Mitigation: Use the documented setup and recovery steps only after a command fails with the matching auth, connection, or billing error. <br>


## Reference(s): <br>
- [Grafana Cloud homepage](https://grafana.com/products/cloud/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-grafana-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands, JSON payload examples, and connector JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector JSON responses when actions run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
