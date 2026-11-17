## Description:

PocketLens helps an agent scan receipts and card statements, record transactions, and answer spending, category, and card-billing questions through PocketLens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edenjw](https://clawhub.ai/user/edenjw)

### License/Terms of Use:

MIT

## Use Case:

External users who track personal expenses use this skill to extract transaction details from receipts, card statements, banking screenshots, or messages and sync them to PocketLens. It also supports connection checks, category lists, spending summaries, and card bill summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt, card statement, and banking screenshots can contain sensitive personal financial details.

Mitigation: Use the skill only with data the user intends to process, and avoid sharing images that contain unrelated account or identity details.

Risk: Extracted transaction details can be incorrect or incomplete before they are sent to PocketLens.

Mitigation: Require the agent to preview merchant, amount, date, card, and category details and obtain user confirmation before creating transactions.

Risk: A full-access API key or untrusted custom API URL can increase the impact of misuse or data exposure.

Mitigation: Use the narrowest suitable API key, avoid full-access keys when possible, and set POCKET_LENS_API_URL only to an endpoint the user controls and trusts.

## Reference(s):

- [PocketLens](https://pocketlens.app)
- [OpenClaw](https://openclaw.ai)
- [ClawHub PocketLens Skill](https://clawhub.ai/edenjw/skills/pocketlens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with inline shell commands and JSON-backed service results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and POCKET_LENS_API_KEY; POCKET_LENS_API_URL is optional.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
