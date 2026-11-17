## Description:

Convert JSON data into clean Markdown tables and reports. Use for pasted JSON, API or log output, or any batch of JSON records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwzhjt](https://clawhub.ai/user/dwzhjt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to convert pasted JSON, API responses, logs, exports, or batches of JSON records into readable Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports from untrusted JSON may remain untrusted documents, especially if later rendered as HTML or opened in viewers that load remote images or allow raw HTML.

Mitigation: Review generated Markdown before publishing or rendering it in permissive viewers, and treat source JSON from unknown parties as untrusted input.

Risk: The local helper reads the JSON file supplied by the user and writes a Markdown report.

Mitigation: Run it only on intended input files and choose output paths that do not overwrite important documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwzhjt/skills/json-report)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown report or Markdown text block with GitHub-style tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a .md report file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
