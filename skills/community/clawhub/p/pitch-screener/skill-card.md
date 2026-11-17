## Description:

Screens startup pitch decks by parsing PDFs, PowerPoint files, or images with SoMark, researching key claims, and producing a concise pre-meeting investment memo with an investment signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and venture teams use this skill to screen inbound pitch decks, prepare before meetings, and batch-review demo day or accelerator decks by combining deck parsing with background research and a concise investment memo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pitch decks and extracted company or founder details may contain confidential financials, customer names, personal founder information, or non-public strategy and may be sent to external services.

Mitigation: Use the skill only after confirming the deck is appropriate for SoMark parsing and web search; request explicit confirmation or a local-only workflow for sensitive decks.

Risk: The generated investment memo could be incomplete or misleading if deck content is missing, external search is unavailable, or claims cannot be independently verified.

Mitigation: Require the memo to distinguish deck evidence, search evidence, contradictions, and unavailable information, and treat the memo as internal screening analysis rather than investment advice.

## Reference(s):

- [Pitch Screener ClawHub page](https://clawhub.ai/soul-code/skills/pitch-screener)
- [SoMark API endpoint](https://somark.tech/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown investment memo with generated Markdown and JSON deck parse files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOMARK_API_KEY; parsed deck content may be sent to SoMark and extracted company or founder details may be used in web searches.]

## Skill Version(s):

1.0.2 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
