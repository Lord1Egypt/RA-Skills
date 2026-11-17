## Description:

Create and manage Google Jules AI coding sessions via the Jules REST API. Start tasks, monitor progress, approve plans, send messages, list sources/repos, and retrieve session activities/artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthbhalodiya](https://clawhub.ai/user/arthbhalodiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, monitor, guide, and retrieve results from Google Jules coding sessions connected to GitHub repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start autonomous coding work against repositories connected to the user's Jules account.

Mitigation: Use plan approval for normal workflows, review prompts and target branches before creating sessions, and avoid auto-PR mode unless it is explicitly needed.

Risk: The skill requires a Jules API key that may grant access to repository operations in connected sources.

Mitigation: Install only for accounts and repositories where this access is intended, and keep the API key in the JULES_API_KEY environment variable rather than hard-coding it.

Risk: The helper script can delete remote Jules sessions without an additional confirmation step.

Mitigation: Check the session ID and current task state before using the delete command.

## Reference(s):

- [Jules API reference](https://jules.google/docs/api/reference/)
- [Jules](https://jules.google)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the JULES_API_KEY environment variable and curl; helper script output is JSON when API calls succeed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
