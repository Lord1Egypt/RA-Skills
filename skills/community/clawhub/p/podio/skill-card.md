## Description:

Helps agents access Podio workspaces, apps, items, tasks, and comments through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to find and manage Podio workspaces, apps, items, tasks, and comments. With explicit approval, they can also arrange recurring Podio actions through Maton automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podio writes or deletions can change or remove business data.

Mitigation: Start with read-only requests and confirm the exact target and effect before every write or deletion.

Risk: Broad connection permissions or exposed API keys can reveal account data.

Mitigation: Use a least-privilege Podio connection and prefer managed login; use a raw API key only when the CLI is unavailable.

Risk: Approved triggers or destinations can keep running and forward data after the initial request.

Mitigation: Obtain separate approval for each automation and destination, including what runs, where data goes, and when it stops.

## Reference(s):

- [Podio skill release](https://clawhub.ai/byungkyu/skills/podio)
- [Maton](https://maton.ai)
- [Podio API documentation](https://developers.podio.com/doc)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Text or Markdown with commands and optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Podio API responses depend on the user's authorized connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
