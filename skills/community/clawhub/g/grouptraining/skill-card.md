## Description:

Likes Training Planner helps agents fetch My Likes training data, analyze training patterns, generate personalized training plans, convert them to Likes format, and push them to a calendar for running, cycling, swimming, and strength training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenwynn](https://clawhub.ai/user/chenwynn)

### License/Terms of Use:

MIT-0

## Use Case:

External athletes, coaches, and developers use this skill to retrieve My Likes activity, feedback, ability, camp, and plan data, analyze training history, generate plan JSON, preview it, and push training plans or coach comments through the Likes API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and setup paths can download executable release artifacts from external URLs.

Mitigation: Avoid curl-to-shell installation; download artifacts separately and verify them before installing.

Risk: The skill uses a Likes API key for data access and write operations.

Mitigation: Protect the LIKES_API_KEY value, prefer managed configuration or environment variables, and rotate the key if it is exposed.

Risk: A custom Base URL can redirect API-key-bearing requests away from the default My Likes service.

Mitigation: Use the default https://my.likes.com.cn endpoint unless the user fully controls and trusts the custom endpoint.

Risk: Plan pushes and coach comments can modify calendar or trainee feedback data, especially from coach accounts.

Mitigation: Use preview_plan.cjs or --dry-run and review plan contents, camp IDs, user IDs, and comment text before pushing changes.

## Reference(s):

- [Likes Open API Documentation](artifact/references/api-docs.md)
- [Likes Training Code Format Reference](artifact/references/code-format.md)
- [Sport-Specific Training Examples](artifact/references/sport-examples.md)
- [My Likes Open API](https://my.likes.com.cn/api/open)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON plan examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce or inspect local JSON plan files and issue Likes API calls when configured with a valid LIKES_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
