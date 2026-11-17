## Description:

Search the web using Google Custom Search Engine (PSE) when live information, documentation, or topical research is needed and built-in web search is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninonano64](https://clawhub.ai/user/ninonano64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform live Google Custom Search queries for documentation lookup, current information, and topical research when a built-in web search tool is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google API credentials may be exposed through command history, logs, request URLs, or unsanitized HTTP errors.

Mitigation: Use a tightly restricted Google API key for Custom Search only, keep credentials in environment or secret storage, avoid inline keys in shell commands, and redact request URLs and HTTP errors before shared logging.

## Reference(s):

- [Google Programmable Search Engine](https://cse.google.com/cse/all)
- [Google Custom Search JSON API endpoint](https://www.googleapis.com/customsearch/v1)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON search results with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and GOOGLE_CSE_ID; default result count is 5.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
