## Description:

Searches installed macOS applications by keyword using Spotlight or common application directories and launches selected apps with the macOS open command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlutwuwei](https://clawhub.ai/user/dlutwuwei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find installed macOS applications, review matching app paths, and launch a selected application from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch macOS applications automatically from an agent workflow.

Mitigation: Require user confirmation before executing open commands, especially when the selected application was inferred from a search result.

Risk: User-provided app names and search text may be mishandled when inserted into shell commands.

Mitigation: Treat app names and search terms as untrusted input, quote arguments safely, and prefer full application paths returned by Spotlight.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlutwuwei/skills/mac-app-launcher)
- [Publisher profile](https://clawhub.ai/user/dlutwuwei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and application path lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run macOS search and launch commands based on user-provided application names or keywords.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
