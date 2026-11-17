## Description:

Read and analyze data from Google Sheets when users provide a sheet link, spreadsheet ID, or sheet-related analysis request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuco99](https://clawhub.ai/user/fuco99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch rows from public or private Google Sheets, cache sheet data locally, and answer questions about spreadsheet contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary flags review concerns around command execution, unsafe cache paths, and plaintext retention of private sheet data.

Mitigation: Review the skill before installing, avoid private sheets unless caching is fixed or disabled, and harden command construction and cache path handling before using untrusted Sheet IDs or attacker-controlled tab names.

Risk: The skill can retain private sheet contents in local cache files.

Mitigation: Use it only with sheets acceptable for the OpenClaw runtime, clear cache after sensitive work, and prefer read-only credentials with the narrowest practical sheet access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuco99/skills/google-sheets-soha)
- [Declared homepage](https://github.com/your-username/google-sheets-soha)
- [Declared repository](https://github.com/your-username/google-sheets-soha)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, inline code, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch Google Sheets data through Google APIs and cache rows locally before answering.]

## Skill Version(s):

1.0.2 (source: server release evidence and target metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
