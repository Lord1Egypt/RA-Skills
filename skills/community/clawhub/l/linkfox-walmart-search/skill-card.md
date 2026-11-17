## Description:

Searches and browses Walmart product listings by keyword, category, price range, sorting, store, and device filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, marketplace analysts, and researchers use this skill to retrieve current Walmart listing data for product discovery, price comparison, availability checks, and competitive research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for a phone number and SMS code during LinkFox onboarding.

Mitigation: Use onboarding only when necessary, confirm the LinkFox service is trusted, and avoid sharing codes outside the intended login flow.

Risk: The skill can expose or persist LinkFox API keys and uses endpoint environment variables.

Mitigation: Keep API keys out of shared logs and repositories, store them in controlled environment variables, and restrict who can modify LinkFox endpoint variables.

Risk: Billing flows can create paid LinkFox orders and each Walmart search consumes credits.

Mitigation: Confirm expected credit usage before high-volume searches and require explicit user approval before creating payment orders.

Risk: Full Walmart search responses are stored locally and may contain detailed product, seller, and query data.

Mitigation: Store results only in appropriate workspaces, review retention needs, and clean local LinkFox data directories when the data is no longer needed.

Risk: The skill may send feedback about user experience or outcomes to LinkFox.

Mitigation: Avoid including sensitive user or business data in feedback content and disclose feedback submission when relevant.

## Reference(s):

- [Walmart Product Search API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-walmart-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown responses with tables and links, JSON API responses, shell commands, configuration snippets, and persisted JSON data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full Walmart search responses are saved under a LinkFox session data directory; small responses may print inline, while larger responses are summarized with sample records.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
