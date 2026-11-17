## Description:

Odoo ERP over XML-RPC for CLI sales, web-order, stock, product, order, and event workflows, with an optional Discuss listener.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crbwi](https://clawhub.ai/user/crbwi)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers use this skill to run Odoo ERP management commands from an agent-controlled terminal, including sales summaries, web-order backlog checks, stock lookup and updates, product creation, order lookup, and event registration counts. The optional Discuss listener can poll Odoo messages and route recognized requests to the same CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Discuss listener can make real ERP changes from broad Odoo Discuss messages without clear authorization or confirmation safeguards.

Mitigation: Treat the listener as privileged automation; install it only for tightly controlled Odoo accounts and test databases unless allowlisted channels or users and explicit confirmations for writes are added.

Risk: Stock updates and product creation can change production Odoo data using the configured account.

Mitigation: Use a least-privilege Odoo account, verify the target Odoo URL and database before execution, and test commands against a non-production database first.

Risk: Product import behavior can fetch external URLs and import HTML or images into Odoo.

Mitigation: Restrict outbound URL fetching to trusted sources, sanitize imported HTML, and prefer draft-only product import until human review is complete.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crbwi/skills/odoo-assistant-manager)
- [README](README.md)
- [Skill manifest](skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command snippets and summarized terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live Odoo XML-RPC operations when required environment variables and account permissions are configured.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact files report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
