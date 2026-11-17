## Description:

Credit card rewards optimizer that helps agents query card data, compare benefits, track a user portfolio, check Chase 5/24 status, and find sign-up bonuses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troyt-666](https://clawhub.ai/user/troyt-666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer credit card rewards questions, compare cards and welcome offers, and manage a local card portfolio. It is intended for US credit card rewards workflows backed by Luca's card database rather than fabricated card details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs the external luca-assistant package from PyPI via uv.

Mitigation: Install only if the publisher and package are trusted, and review the package source or lock deployment inputs before use.

Risk: Portfolio actions can persistently add, close, import, or update card data in a local database.

Mitigation: Have the agent confirm before performing portfolio write actions or refreshing card data.

Risk: Credit card offer or rule data may be stale or incomplete.

Mitigation: Use database-backed answers, refresh data when appropriate, and avoid guessing when a card is not found.

## Reference(s):

- [Luca Assistant project homepage](https://github.com/troyt-666/luca-assistant)
- [Luca Assistant ClawHub listing](https://clawhub.ai/troyt-666/skills/luca-assistant)
- [nitan companion skill](https://clawhub.ai/nitansde/nitan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional shell command examples and JSON-formatted MCP tool arguments or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call luca-mcp tools and update a persistent local portfolio database at ~/.local/share/luca/luca.db.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
