## Description:

Downloads main drawings for Chinese patents and creates a browsable gallery with patent titles and abstracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent researchers, analysts, and product teams can download drawings for a supplied patent list or a technology search, then review the results in a gallery before selecting figures for further analysis or presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API requests can expose credentials or reach unintended destinations if transport and redirects are not checked.

Mitigation: Require HTTPS, restrict requests to approved destinations, validate redirects, and provide keys through a protected environment rather than chat or command history.

Risk: Saved credentials and cache or output paths may be exposed or access files outside the intended directory.

Mitigation: Protect any saved key and enforce path containment checks for cache and generated files.

Risk: Search terms and batch size can disclose sensitive topics or trigger unexpected charges.

Mitigation: Use nonconfidential search terms and agree on the quantity and cost before starting paid searches or downloads.

## Reference(s):

- [Skill usage and workflow](artifact/SKILL.md)
- [Search workflow](artifact/references/search-workflow.md)
- [Query syntax](artifact/references/query-syntax.md)
- [API reference](artifact/references/api-reference.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Publisher service](https://ip930.com)

## Skill Output:

**Output Type(s):** [Files, Images, HTML, CSV, Guidance]

**Output Format:** [PNG patent drawings, an HTML gallery, a UTF-8 CSV inventory, and brief usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on patent data and drawing availability from the provider; searches and downloads may incur fees.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
