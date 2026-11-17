## Description:

Interact with KitchenOwl APIs (login, token handling, REST/GraphQL calls, and shopping-list read/update) through a reusable CLI script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pietro395](https://clawhub.ai/user/pietro395)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect to self-hosted or cloud KitchenOwl instances, authenticate, inspect API endpoints, and read or update shopping-list data through REST or GraphQL calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles KitchenOwl passwords and saved access or refresh tokens.

Mitigation: Prefer HTTPS KitchenOwl URLs, avoid passing credentials where shell history or process listings may expose them, and review permissions on ~/.config/kitchenowl-api/session.json.

Risk: Generic REST and GraphQL commands can perform account or data changes beyond shopping-list updates.

Mitigation: Review each request method, path, and JSON body before execution, and use the least-privileged KitchenOwl account or token available.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; may save KitchenOwl session tokens under ~/.config/kitchenowl-api/session.json.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
