## Description:

Crossref (crossref.org). Use this skill for ANY Crossref request — searching and reading data. Whenever a task involves Crossref, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, librarians, and developers can use this skill to search and retrieve Crossref records, inspect DOI metadata, find matching works for references, and export citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code that has not been verified, without clear user approval.

Mitigation: Review and pin the CLI before installation, require approval for installation changes, and check its automatic skill synchronization settings.

Risk: Crossref queries and references routed through OOMOL may incur charges.

Mitigation: Check applicable OOMOL billing and credit before running queries.

## Reference(s):

- [Crossref](https://www.crossref.org/)
- [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Markdown, Code]

**Output Format:** [Structured Crossref metadata and citation exports, including BibTeX, RIS, CSL JSON, formatted citations, RDF, Turtle, and UNIXREF XML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Crossref action and may include an execution identifier.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
