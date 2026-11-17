## Description:

Atomic node skill to search for emails in Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search a connected Gmail account for specific emails or communications and return matching email headers and snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search sensitive mailbox content and return message snippets under a broad trigger.

Mitigation: Confirm the Gmail account, search query, and whether snippets should be returned before running the search.

Risk: Search results may expose personal or confidential email metadata.

Mitigation: Share or persist only the minimum result fields needed for the user's task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-search-emails)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [JSON array of email headers and snippets, or a no-results message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and access to the intended Gmail account.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
