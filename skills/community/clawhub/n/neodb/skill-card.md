## Description:

Search, mark, rate, and review books, movies, music, games on NeoDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitnapp](https://clawhub.ai/user/gitnapp)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to manage a NeoDB account through the NeoDB API, including catalog search, shelf marks, ratings, reviews, notes, collections, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth setup flow may expose or persist live NeoDB credentials.

Mitigation: Use a secure secret store for tokens, avoid logging credentials, and revoke or rotate any token that may have been printed, stored in shell history, captured in session logs, backed up, or written to artifact/scripts/.credentials.json.

Risk: The skill can perform read and write operations on a NeoDB account.

Mitigation: Install only after review, grant access only to accounts where this level of access is acceptable, and require user confirmation before write actions.

## Reference(s):

- [NeoDB Skill Page](https://clawhub.ai/gitnapp/skills/neodb)
- [NeoDB API](https://neodb.social)
- [Catalog API Reference](references/catalog.md)
- [Shelf and Journal API Reference](references/shelf-and-journal.md)
- [Collection and Tag API Reference](references/collection-and-tag.md)
- [Official OpenAPI Spec](references/openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a NeoDB OAuth token; write actions should be confirmed with the user before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
