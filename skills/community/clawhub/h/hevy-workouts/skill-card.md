## Description:

Interact with the Hevy fitness app via the hevy-cli command-line tool to view, create, or update workouts, routines, exercise templates, and routine folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sajal2692](https://clawhub.ai/user/sajal2692)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect Hevy workout history and manage workouts, routines, exercise templates, and routine folders through the hevy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a user's Hevy fitness account.

Mitigation: Install only when the agent is expected to access that account, and limit requests to the intended workout, routine, exercise template, or folder task.

Risk: The documented --api-key flag can expose credentials in command history or process listings.

Mitigation: Prefer HEVY_API_KEY or a secret manager instead of passing the API key as a command flag.

Risk: Create and update commands can persistently change workouts, routines, exercise templates, or folders.

Mitigation: Require the agent to show the exact planned create or update command and obtain confirmation before making changes.

## Reference(s):

- [Hevy CLI Command Reference](artifact/references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that read or change Hevy account data; account-changing commands should be shown for confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
