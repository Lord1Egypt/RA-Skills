## Description:

Use Hydrafetch for live web scraping, site mapping, search, structured extraction, brand and logo lookup, design systems, screenshots, and bulk crawl or batch jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hydrafetch](https://clawhub.ai/user/hydrafetch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current public-web information, convert pages into clean Markdown, extract typed JSON from websites, inspect brand assets, and run larger crawl or batch web-processing jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hydrafetch handles submitted URLs, search queries, extraction schemas, and fetched targets through an external scraping API.

Mitigation: Configure HYDRAFETCH_API_KEY only in environments where sending those inputs to Hydrafetch is appropriate.

Risk: Fetched page content can contain untrusted or misleading instructions.

Mitigation: Treat scraped content as data, preserve source URLs, and distinguish page claims from agent inferences.

Risk: API credentials could be exposed if printed, logged, hardcoded, or placed in client-side code.

Mitigation: Read the credential from HYDRAFETCH_API_KEY and avoid emitting the key in logs, generated code, or user-visible output.

## Reference(s):

- [Hydrafetch Skill Page](https://clawhub.ai/hydrafetch/skills/hydrafetch)
- [Hydrafetch Documentation Index](https://hydrafetch.com/llms.txt)
- [Hydrafetch Agent Reference](https://hydrafetch.com/agents.md)
- [Hydrafetch API Documentation](https://docs.hydrafetch.com)
- [Hydrafetch OpenAPI Specification](https://api.hydrafetch.com/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs, response metadata, structured extraction output, crawl or batch job identifiers, and next commands for inspecting asynchronous results.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
