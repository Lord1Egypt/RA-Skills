## Description:

Use this skill when the user asks about reading highlights, book notes, annotations, or reading history from KOReader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myugan](https://clawhub.ai/user/myugan)

### License/Terms of Use:


## Use Case:

External users and reading-focused agents use this skill to find, list, search, and summarize KOReader HighlightSync annotations from a local Dropbox-synced library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims to be read-only but also instructs the agent to update memory/profile files and delete a bootstrap file.

Mitigation: Remove or gate file-writing and deletion behavior before deployment; allow only explicit, user-approved workspace memory updates if needed.

Risk: The skill uses command templates that interpolate paths, app names, and search terms.

Mitigation: Use safe argument handling, validate inputs, and constrain reads to the intended KOReader HighlightSync directory.

Risk: The skill requires technical execution and errors to be hidden from the user.

Mitigation: Keep end-user replies human-readable while preserving enough auditability for operators to review failures and unexpected local execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Human-readable text or short Markdown lists for book titles, highlight excerpts, page numbers, dates, chapters, and summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to hide raw commands, code, JSON, file paths, and technical errors from the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
