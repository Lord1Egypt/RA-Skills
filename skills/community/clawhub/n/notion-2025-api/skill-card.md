## Description:

Query, create, and manage Notion databases and pages using the 2025-09-03 API format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-tw](https://clawhub.ai/user/kai-tw)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query Notion data sources, create database entries, update page properties, and add page content blocks through the Notion 2025-09-03 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived Notion API key stored in a local plaintext file.

Mitigation: Use a least-privilege Notion integration, restrict shared pages and databases, set restrictive file permissions, and rotate the token if exposure is suspected.

Risk: Write and batch operations can alter more Notion data than intended.

Mitigation: Review write commands before execution, test against non-critical pages first, and share only the specific Notion pages or databases required.

Risk: Untrusted property names, filters, or JSON payloads can produce malformed or unsafe Notion requests.

Mitigation: Avoid passing untrusted input directly to the helper script; validate JSON and escape user-provided text with jq before use.

## Reference(s):

- [Notion 2025-09-03 API Reference](references/API_REFERENCE.md)
- [Notion 2025 API Examples](references/EXAMPLES.md)
- [Notion Integration Setup](https://notion.so/my-integrations)
- [ClawHub Skill Page](https://clawhub.ai/kai-tw/skills/notion-2025-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Notion API endpoints through curl and parse responses with jq when the user provides valid Notion identifiers and credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
