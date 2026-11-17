## Description:

Search and read BaseLinker inventory and order data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

BaseLinker users and operators can use the skill to retrieve inventory catalogs, products, warehouses, order events, statuses, and filtered orders from an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional setup fallback executes remote CLI installer code.

Mitigation: Review and approve the CLI installation separately before using the setup fallback.

Risk: The security guidance identifies cross-agent skill synchronization as a possible unwanted behavior.

Mitigation: Disable the documented cross-agent skill synchronization if it is not wanted.

Risk: Actions can retrieve business data from the connected BaseLinker account.

Mitigation: Connect only the intended BaseLinker account through OOMOL.

## Reference(s):

- [BaseLinker](https://baselinker.com)
- [BaseLinker API documentation](https://api.baselinker.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance, oo CLI commands, and JSON action payloads and responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only inventory and order data; the list_orders action returns up to 100 orders.]

## Skill Version(s):

1.0.6 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
