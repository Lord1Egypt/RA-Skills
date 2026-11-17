## Description:

Use when a user wants to track expenses, scan receipts, upload card payment screenshots, categorize spending, record transactions, check spending summaries, view card billing amounts, or query monthly expense breakdowns via PocketLens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edenjw](https://clawhub.ai/user/edenjw)

### License/Terms of Use:


## Use Case:

External PocketLens users use this skill in OpenClaw to turn receipt images, card statements, and natural-language expense descriptions into PocketLens transactions, then review categories, monthly spending summaries, and card billing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial data from receipts, card statements, and payment screenshots.

Mitigation: Redact unnecessary card, account, and statement details before upload, and confirm extracted transactions before recording them.

Risk: The skill uses a write-capable PocketLens API key to create transactions.

Mitigation: Use a write-only key rather than full access, rotate it if exposed, and avoid sharing command output that may reveal account details.

Risk: The security summary flags unsafe command and endpoint handling, including optional custom API URLs.

Mitigation: Avoid setting a custom API URL unless the server is fully trusted, and review command arguments before execution.

## Reference(s):

- [PocketLens homepage](https://pocketlens.app)
- [OpenClaw](https://openclaw.ai)
- [PocketLens ClawHub skill page](https://clawhub.ai/edenjw/skills/pocket-lens)
- [edenjw ClawHub publisher profile](https://clawhub.ai/user/edenjw)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with JSON helper-script results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and POCKET_LENS_API_KEY; can use POCKET_LENS_API_URL to target a custom API base URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
