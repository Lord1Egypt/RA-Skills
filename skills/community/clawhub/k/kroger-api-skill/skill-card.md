## Description:

Search Kroger/QFC products, manage a local cart, check pickup availability, and create pickup orders through the Kroger API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonahorn](https://clawhub.ai/user/jasonahorn)

### License/Terms of Use:


## Use Case:

Developers and shopping agents use this skill to search Kroger/QFC inventory, select stores and pickup slots, manage grocery cart state, and prepare pickup orders with user-provided Kroger API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials and tokens may be stored in local plaintext state.

Mitigation: Use the skill only in a trusted private workspace, keep state.json out of sync folders and source control, and revoke Kroger credentials if the file is exposed.

Risk: The skill can clear cart state or create live pickup orders without a documented confirmation step.

Mitigation: Require the agent to show cart contents, store, pickup time, and final action before any cart clear or pickup order creation.

## Reference(s):

- [Kroger Developer Portal](https://developer.kroger.com)
- [Kroger API Reference](https://developer.kroger.com/reference)
- [ClawHub Skill Page](https://clawhub.ai/jasonahorn/skills/kroger-api-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local state file for OAuth tokens, cart contents, location ID, and chain ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
