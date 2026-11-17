## Description:

Manage Trello boards, lists, and cards via the Trello REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Trello users can use this skill to inspect boards, lists, and cards, and to create, move, comment on, or archive cards through Trello's REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Trello API key and token enable account access, and the examples include actions that create, update, comment on, and archive cards.

Mitigation: Keep the credentials secret, use the skill only when you intend to connect to Trello, and review each write action and its board or card identifiers before running it.

## Reference(s):

- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello API key and token setup](https://trello.com/app-key)
- [Trello skill release on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-trello)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline curl and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a Trello API key and token and can read or change board and card data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
