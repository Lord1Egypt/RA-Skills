## Description: <br>
Operates Grafana through OOMOL's oo CLI for reading, creating, updating, and deleting dashboards, folders, and data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Grafana resources through an OOMOL-connected account. It helps inspect live action schemas, build valid JSON payloads, and run read, write, and delete connector actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Grafana account through OOMOL-managed credentials. <br>
Mitigation: Install it only if you trust OOMOL and use a least-privileged Grafana service account where possible. <br>
Risk: Write and destructive actions can change or remove Grafana dashboards, folders, and data sources. <br>
Mitigation: Inspect the live connector schema, review the exact payload and target, and require explicit approval before delete actions. <br>


## Reference(s): <br>
- [Grafana homepage](https://grafana.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-grafana) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL sign-in, and a connected Grafana account; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
