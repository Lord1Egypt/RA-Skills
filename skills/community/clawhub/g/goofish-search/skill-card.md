## Description:

Use when user wants to search Xianyu/Goofish for products. Auto-search, filter merchants, sort by price, and output TOP results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mabe88650](https://clawhub.ai/user/mabe88650)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting shoppers use this skill to search Xianyu/Goofish for second-hand products, filter out merchant-style listings and ads, sort by price, and return concise top results with item links and price statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a logged-in Goofish browser session, so searches and clicks occur under the user's active account.

Mitigation: Use the intended browser profile and review actions before allowing purchase-related or account-sensitive steps.

Risk: Search results, including item links, may be saved locally as a Markdown file.

Mitigation: Review or adjust the save location when local records of shopping searches should not be retained.

Risk: Goofish page structure and pagination controls can change, which may reduce filtering accuracy or page traversal reliability.

Mitigation: Review the generated results and update selectors or browser interaction steps when the site layout changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mabe88650/skills/goofish-search)
- [Goofish DOM structure reference](artifact/references/goofish-dom-structure.md)
- [Goofish search URL pattern](https://www.goofish.com/search?q={keyword})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with tables, item links, filtering notes, and local file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a Markdown results file to the user's desktop path described by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
