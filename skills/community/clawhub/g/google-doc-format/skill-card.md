## Description:

Create professionally formatted Google Docs from markdown using gog docs create, including heading hierarchy, native tables, bold text, bullet and numbered lists, and clickable hyperlinks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandrainmakerai](https://clawhub.ai/user/brandrainmakerai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to turn markdown drafts into properly formatted Google Docs, especially for structured reports, deliverable indexes, and documents with tables or links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes forced Google Drive rename, move, and delete commands that can change or remove existing documents.

Mitigation: Require confirmation of exact document IDs and document names before replacements, and keep a backup or archive before deleting an old document.

Risk: The skill creates or modifies Google Docs through the user's gog credentials.

Mitigation: Install and run it only when the user intentionally wants the agent to operate on Google Docs with those credentials.

Risk: Temporary markdown files may expose document contents if written to a shared path.

Mitigation: Use a private temporary file or directory for source markdown instead of a predictable shared path such as /tmp/doc_name.md.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses gog commands to create, inspect, rename, move, or delete Google Docs and Drive files when the user authorizes those actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
