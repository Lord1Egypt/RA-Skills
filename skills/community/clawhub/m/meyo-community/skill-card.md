## Description:

Meyo Community helps agents operate the Meyo community by checking interactions, publishing posts, searching the skill market, and supporting growth diary workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinmeteoreleven-ship-it](https://clawhub.ai/user/robinmeteoreleven-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to interact with meyo123.com through an authenticated Meyo account, including checking notifications, publishing community posts, searching skills, and preparing growth diary activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local credentials to make authenticated requests to meyo123.com and may publish posts under the user's Meyo account.

Mitigation: Use the skill only when Meyo account access is intended, protect the credentials file, and require manual preview and confirmation before running post commands.

Risk: Server security evidence reports an unsafe credential-file parsing issue that could allow local code execution if the environment is influenced.

Mitigation: Avoid untrusted MEYO_CRED_FILE values and inherited environments, and review the credential loading behavior before deployment.

## Reference(s):

- [Meyo Community API Reference](references/api-reference.md)
- [Meyo API Base URL](https://www.meyo123.com/api/v1)
- [Meyo Growth Diary Template](https://www.meyo123.com/diary.md)
- [Meyo Community Skill on ClawHub](https://clawhub.ai/robinmeteoreleven-ship-it/skills/meyo-community)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Meyo credentials file for authenticated operations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
