## Description:

Find a product on the Lululemon Australia site from a natural-language clothing description and return structured details such as product name, variant colors, sizes, prices, URLs, and provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ensonfun](https://clawhub.ai/user/ensonfun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to find Lululemon Australia products from fuzzy clothing descriptions and return structured product, variant, price, size, URL, and field-source details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional browser-session fallback may expose browser state to the agent during a shopping lookup.

Mitigation: Use browser-session fallback only with a session the user is comfortable letting the agent access; prefer official search discovery and product pages first.

Risk: Anti-bot blocks can force partial product answers based on official snippets or sibling variants.

Mitigation: Return confidence, coverage, sources, and per-field provenance so users can distinguish product-page data from fallback-derived data.

## Reference(s):

- [Lululemon Australia homepage](https://www.lululemon.com.au/en-au/home)
- [ClawHub skill page](https://clawhub.ai/ensonfun/skills/lululemon-au-product-finder)
- [Lululemon AU Anti-Bot And Data Source Notes](references/anti-bot-and-sources.md)
- [Lululemon AU Fallback Ladder](references/fallback-ladder.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured JSON-style product object with explanatory notes and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-field provenance, confidence, and coverage indicators for partial or fallback-derived product data.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
