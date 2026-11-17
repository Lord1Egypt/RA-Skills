## Description:

Money Forward Cloud Accounting MCP (developers.biz.moneyforward.com). Use this skill for ANY Money Forward Cloud Accounting MCP request — reading, creating, and updating data. Whenever a task involves Money Forward Cloud Accounting MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and accounting staff use the skill to inspect Money Forward Cloud Accounting offices, accounts, transactions, journals, and financial reports, and to create or update ledger records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer and hosted connector implementation were not verified.

Mitigation: Review and install a verified CLI release separately before using the skill.

Risk: Startup skill synchronization may make broader changes to installed agent skills.

Mitigation: Consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the CLI reference.

Risk: Accounting data may be processed by OOMOL, and write actions can change ledger records.

Mitigation: Limit connected-account permissions and review every ledger change before confirming it.

## Reference(s):

- [Money Forward Cloud Accounting MCP documentation](https://developers.biz.moneyforward.com/mcp/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-moneyforward-mcp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON payloads or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can retrieve accounting data and prepare ledger changes; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
