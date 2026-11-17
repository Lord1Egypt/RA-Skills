## Description:

Interact with Mealie recipe manager (recipes, shopping lists, meal plans). Self-hosted recipe and meal planning API client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusthefuzz](https://clawhub.ai/user/angusthefuzz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent work with a self-hosted Mealie instance for recipe lookup, shopping list updates, meal planning, and household recipe management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete or modify Mealie recipes, shopping list items, and meal plans.

Mitigation: Review agent-proposed destructive actions before execution and use a dedicated least-privilege Mealie API token.

Risk: The Mealie API token may be sent over unencrypted HTTP if MEALIE_URL is configured with an http:// URL.

Mitigation: Configure MEALIE_URL with HTTPS only and store the token in an .env file with restrictive permissions.

## Reference(s):

- [Mealie project website](https://mealie.io)
- [Mealie documentation](https://docs.mealie.io)
- [ClawHub skill page](https://clawhub.ai/angusthefuzz/skills/mealie-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Terminal text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node plus MEALIE_URL and MEALIE_API_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
