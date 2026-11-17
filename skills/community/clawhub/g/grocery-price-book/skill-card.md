## Description:

Builds a local grocery price book from manual entries or receipt text, normalizes unit prices, tracks price history, flags shrinkflation, ranks stores by the user's basket, and evaluates bulk-buy or membership breakeven decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and household shoppers use this skill to maintain a local grocery price history, compare unit prices across stores and package sizes, identify price increases or shrinkflation, and decide whether bulk purchases or store memberships are financially worthwhile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt-derived grocery data may reveal household shopping patterns and is stored in a local JSON file.

Mitigation: Keep the local pricebook file private, avoid sharing it unintentionally, and delete the file when resetting or removing the skill's stored data.

Risk: Receipt parsing can misread item names, quantities, prices, or package sizes because receipt formats vary.

Mitigation: Review parsed receipt lines before importing and correct item names, quantities, prices, or sizes before relying on unit-price, shrinkflation, bulk-buy, or membership calculations.

## Reference(s):

- [README](README.md)
- [The Price Book Method Reference](references/method-guide.md)
- [Receipt Example](references/receipt-example.txt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [CLI text reports, JSON analysis output, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered grocery and receipt-derived price history in a local JSON file.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
