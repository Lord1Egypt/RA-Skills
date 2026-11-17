## Description:

Search and read Terraform account, organization, workspace, and run data through OOMOL's oo CLI connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to inspect Terraform organizations, workspaces, runs, and account details through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes remote CLI installers without first requesting approval.

Mitigation: Install a reviewed, pinned CLI release yourself and review any changes it makes before use.

Risk: OOMOL brokers access to the connected Terraform account.

Mitigation: Use a Terraform API key limited to the reads you need and understand that OOMOL brokers the account access.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Terraform](https://www.hashicorp.com/products/terraform)
- [Terraform Cloud API documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-terraform)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Terraform account, organization, workspace, and run data; inputs follow the selected action's schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
