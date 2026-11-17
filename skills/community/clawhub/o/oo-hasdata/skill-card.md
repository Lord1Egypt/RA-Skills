## Description:

HasData (hasdata.com). Use this skill for ANY HasData request — searching and reading data. Whenever a task involves HasData, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Google results and scrape public web pages through a connected HasData account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code whose behavior has not been verified.

Mitigation: Arrange CLI setup separately using a verified release and review its local changes.

Risk: Automatic synchronization may change additional agent skills without clear user control.

Mitigation: Check synchronization settings and disable automatic synchronization if it is not wanted.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [HasData Web Scraping API quickstart](https://docs.hasdata.com/apis/web-scraping-api/quickstart)
- [HasData](https://hasdata.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected search or scraping action and connected account access.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
