## Description:

Searches a user's local OMem work-memory index across configured emails, calendar events, documents, and collaboration notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seacen](https://clawhub.ai/user/seacen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to answer questions about their own work history by querying a local OMem wiki, then fetching the most relevant pages or parsed source text when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface confidential local work-history material from email, calendar, document, and collaboration sources.

Mitigation: Use it only for clearly work-history-related questions and review retrieved content before sharing it outside the user's intended context.

Risk: Untrusted user text could be passed into local shell queries.

Mitigation: Quote query strings carefully and avoid pasting untrusted text directly into shell commands.

Risk: The artifact includes curl-to-shell installation guidance for the prerequisite OMem CLI.

Mitigation: Prefer a verified or package-managed installer before enabling the skill in sensitive environments.

## Reference(s):

- [OMem documentation](https://seacen.github.io/omem/)
- [Query syntax](references/query-syntax.md)
- [Output schemas](references/output-schemas.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with citations and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON output from the local omem CLI and may cite OMem wiki or source paths.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
