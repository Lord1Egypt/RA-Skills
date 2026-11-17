## Description:

Patent marketplace via trade.9235.net for listings, sellers, deal history, open licensing, procurement, and Excel export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windinwing](https://clawhub.ai/user/windinwing)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query a patent marketplace for listed patents, seller information, deal records, open licenses, and procurement demand during patent transfer or licensing due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends patent marketplace queries to trade.9235.net using TRADE_API_TOKEN.

Mitigation: Review before installing in shared or sensitive environments and prefer header-based token authentication.

Risk: The skill can automatically install an unpinned spreadsheet package at runtime.

Mitigation: Install openpyxl through a controlled, pinned dependency process before deployment.

Risk: Exported spreadsheets may contain untrusted marketplace data.

Mitigation: Avoid opening exported spreadsheets without formula-injection protections and review exported transaction data before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windinwing/skills/patent-transaction)
- [Publisher profile](https://clawhub.ai/user/windinwing)
- [Trade marketplace homepage](https://trade.9235.net)
- [Trade Skill API endpoint](https://trade.9235.net/api/skill)
- [Due diligence checklist](due-diligence.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, files, configuration guidance]

**Output Format:** [Markdown tables, strings, JSON-like tool responses, and Excel or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRADE_API_TOKEN for the default API path; exported transaction data is written under trade-exports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
