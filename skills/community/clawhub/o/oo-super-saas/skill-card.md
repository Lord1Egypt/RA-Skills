## Description:

Search and read SuperSaaS data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected SuperSaaS account can retrieve schedules, appointments, fields, groups, resources, recent changes, and SuperForms. The skill guides the agent to inspect each action's live schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded software, and the installers and hosted connector implementation were not inspected.

Mitigation: Review and install a verified oo CLI release yourself, require approval before any fallback installation, and review OOMOL's access to the connected SuperSaaS account.

## Reference(s):

- [SuperSaaS](https://www.supersaas.com/)
- [SuperSaaS API authentication documentation](https://www.supersaas.com/info/dev/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured connector results with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented SuperSaaS account data; the skill documents no write or destructive actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
