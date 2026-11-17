## Description:

Interact with a self-hosted Mealie instance via its REST API for recipe management, meal planning, and shopping-list retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1mb01d](https://clawhub.ai/user/g1mb01d)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to work with their own Mealie server from an agent session, including importing recipes, retrieving recipes, creating meal plans, and fetching shopping lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API actions can write recipes and meal plans to the user's Mealie account.

Mitigation: Confirm the target Mealie URL and intended account-changing operation before running add-recipe or create-plan.

Risk: A broad or exposed Mealie token could allow unintended account access.

Mitigation: Use HTTPS, prefer the least-privileged token available, keep MEALIE_TOKEN out of files and logs, and rotate it when needed.

Risk: The artifact only contains markdown instructions even though it describes a helper script.

Mitigation: Review or create any helper script locally before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g1mb01d/skills/mealie)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment-variable configuration, and JSON-oriented API payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided MEALIE_URL and MEALIE_TOKEN before account-specific API actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
