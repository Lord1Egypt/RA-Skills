## Description:

Searches and retrieves Google Patents data through SerpApi for patent research, infringement risk checks, competitive IP analysis, and PDF retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:


## Use Case:

Developers, patent researchers, and e-commerce operators use this skill to search patents, inspect claims and descriptions, assess freedom-to-operate concerns, track competitor patents, and download patent PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships an embedded fallback SerpApi key.

Mitigation: Remove or rotate the fallback key and require users to provide their own SERPAPI_API_KEY before use.

Risk: Patent queries and fetched patent URLs are sent to external services.

Mitigation: Avoid confidential patent queries unless disclosure to SerpApi and fetched patent URLs is acceptable.

Risk: The PDF command can write to a caller-selected filesystem path.

Mitigation: Use constrained, reviewed output paths and run the skill only where overwrite impact is limited.

## Reference(s):

- [Google Patents skill release on ClawHub](https://clawhub.ai/jiafar/skills/google-patents)
- [SerpApi Search API endpoint used by the skill](https://serpapi.com/search.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, Files]

**Output Format:** [JSON responses, text output, and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, detail, fulltext, and full commands return patent data; the pdf command writes a PDF to a caller-selected path.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
