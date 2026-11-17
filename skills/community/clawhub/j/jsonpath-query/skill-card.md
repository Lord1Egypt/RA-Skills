## Description:

Query JSON data using JSONPath expressions to extract, filter, search, or navigate JSON data with recursive descent, wildcards, array slicing, filter expressions, and union selections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query JSON files or stdin, list available JSONPath paths, validate JSONPath expressions, and extract named values for inspection, scripting, or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can print values from user-provided JSON files, including sensitive data if those files contain it.

Mitigation: Run the skill only on files whose contents are intended to be visible in the agent or terminal output, and avoid querying secrets or sensitive records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/jsonpath-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSONPath examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI can print JSON, text, line-delimited output, CSV rows, path lists, expression validation details, and named extraction results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
