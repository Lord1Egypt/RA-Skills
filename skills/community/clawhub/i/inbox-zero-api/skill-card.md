## Description:

Use the Inbox Zero API CLI to inspect the live API schema, list and manage automation rules, and read inbox analytics through the public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elie222](https://clawhub.ai/user/elie222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect or change Inbox Zero state through the public API, including automation rules, live API schema details, and inbox analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke an unpinned npm CLI with an API key.

Mitigation: Prefer a pinned, reviewed @inbox-zero/api version and use a revocable, least-privilege API key stored in INBOX_ZERO_API_KEY or configured skill settings.

Risk: The skill can modify or delete live mail automation rules.

Mitigation: Inspect the live schema, read and back up the existing rule before update or delete, and treat rule updates as full replacements.

Risk: Rule JSON files may expose sensitive automation details in shared or synced workspaces.

Mitigation: Keep rule JSON in an appropriate workspace location and remove temporary files after review and application.

## Reference(s):

- [Inbox Zero CLI API Reference](https://www.getinboxzero.com/api-reference/cli)
- [ClawHub skill page](https://clawhub.ai/elie222/skills/inbox-zero-api)
- [CLI reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers --json output for stable machine-readable command results.]

## Skill Version(s):

2.29.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
