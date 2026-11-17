## Description:

Use the oo CLI with an OOMOL-connected Grafana account to read and manage Grafana dashboards, folders, data sources, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Grafana users can use this skill to inspect dashboards, folders, data sources, and alerting information, and to create, update, or delete supported Grafana resources through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and may introduce broader changes to installed agent skills.

Mitigation: Review setup before installing, use a pinned and verified CLI installed under your control, and disable startup skill synchronization if you do not want other agent skills changed.

Risk: The hosted connector was not verified, and an over-permissioned Grafana API key could grant access beyond what the task needs.

Mitigation: Grant only the necessary API-key permissions and review the connector setup before use.

Risk: Grafana writes and deletions can change or remove resources.

Mitigation: Keep the skill's explicit approval requirements for write and destructive actions.

## Reference(s):

- [Grafana skill release](https://clawhub.ai/oomol/skills/oo-grafana)
- [Grafana](https://grafana.com)
- [Grafana HTTP API documentation](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read Grafana information and, with user approval, make changes or delete resources.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
