## Description: <br>
New Relic (newrelic.com). Use this skill for New Relic requests that read, create, update, or delete data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to inspect and manage New Relic observability resources through the OOMOL new_relic connector. It supports NRQL queries, entity search, dashboards, alert policies, synthetics monitors, deployment markers, and secure credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a New Relic account through a connected API key. <br>
Mitigation: Install only if you trust OOMOL and intend to grant this agent access to the connected New Relic account. <br>
Risk: Write and destructive actions can create, replace, update, or delete New Relic dashboards, alert policies, NRQL conditions, monitors, secure credentials, snapshots, and deployment markers. <br>
Mitigation: Review the exact target and payload before approving writes or deletes, and require explicit confirmation for destructive operations. <br>
Risk: Dashboard replacement, alert-policy changes, monitor deletion, or secure-credential updates can disrupt observability workflows. <br>
Mitigation: Inspect existing state with read actions first, fetch the live action schema before constructing payloads, and keep approvals scoped to the intended resource. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-new-relic) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [New Relic](https://newrelic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run oo CLI connector schema and connector run commands that return JSON responses from New Relic.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
