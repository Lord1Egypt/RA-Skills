## Description:

Formats, validates, minifies, and extracts JSONPath-style paths from JSON content to improve readability and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and automation users use this skill to inspect API responses, validate JSON syntax, minify configuration payloads, and extract JSON paths for downstream mapping or debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, execute, and write tools for a JSON formatter.

Mitigation: Review the skill before installation and run it with the least tool access needed for formatting, validation, minification, and path extraction.

Risk: The skill asks users to configure an API key without documenting a specific trusted service that requires it.

Mitigation: Do not provide credentials unless the operator has confirmed a trusted service and a concrete need for the key.

Risk: JSON inputs may contain secrets, tokens, or private data that could appear in formatted output, logs, or examples.

Mitigation: Avoid processing sensitive payloads unless the execution environment, logging, and output handling are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-beautifier)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like text examples with inline shell or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces formatted JSON, validation findings, compact JSON, JSONPath-style paths, and usage guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
