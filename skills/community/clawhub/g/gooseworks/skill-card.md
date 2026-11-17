## Description:

GooseWorks is a data toolkit for searching, scraping, lead generation, prospect research, enrichment, and related go-to-market research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akhilathina](https://clawhub.ai/user/akhilathina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and go-to-market teams use this skill to find and enrich people, company, social, website, and market data through GooseWorks-hosted catalog skills and APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GooseWorks can download catalog-provided scripts and files and run them locally while credentials are available.

Mitigation: Use the skill in a sandbox or disposable environment, inspect fetched content, and require explicit approval before downloading code, installing dependencies, or running scripts.

Risk: Data tasks and API calls may send prompts, query parameters, and other task data through GooseWorks services and can trigger billed API usage.

Mitigation: Avoid sensitive prompts or private datasets, verify the API base before authenticating, and require user approval before billed API calls.

## Reference(s):

- [GooseWorks ClawHub Skill Page](https://clawhub.ai/akhilathina/skills/gooseworks)
- [GooseWorks Homepage](https://github.com/gooseworks-ai/gooseworks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, and structured data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local scripts, configuration files, CSVs, reports, and data exports when a fetched GooseWorks catalog skill requires them.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
