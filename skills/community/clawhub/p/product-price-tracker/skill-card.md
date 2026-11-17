## Description:

Tracks product price changes, compares them with historical records, and generates reports for competitor monitoring, price-drop checks, and price trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and procurement teams use this skill to track product or competitor prices, record manually verified price observations, compare them with historical values, and generate periodic reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default storage uses local files under /tmp, which may be temporary or shared on some systems.

Mitigation: Set PRICE_DB_FILE and PRICE_SCREENSHOT_DIR to a private, user-owned persistent directory before regular use.

Risk: The skill does not fully automate price scraping or notifications without additional agent or tool automation.

Mitigation: Verify search results and recorded prices before relying on reports for purchasing or competitive analysis.

Risk: Product removal is name-based and can delete a tracked item if the wrong name is supplied.

Mitigation: List tracked products and verify the exact product name before using --remove.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/skills/product-price-tracker)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown-style reports with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores product records and price history in a local JSON file; PRICE_DB_FILE and PRICE_SCREENSHOT_DIR can be set for custom storage paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
