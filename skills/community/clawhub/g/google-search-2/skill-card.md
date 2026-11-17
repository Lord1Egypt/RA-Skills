## Description:

Perform global web searches using the Google Custom Search API with configurable result counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current web search results for news, research, product, and academic queries through Google Custom Search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google API keys or sensitive query details may appear in provider errors or returned URLs.

Mitigation: Use a dedicated restricted Google Custom Search key, avoid sensitive searches, and review or adjust error handling before deployment.

Risk: The skill sends search queries to Google Custom Search.

Mitigation: Do not submit confidential prompts, customer data, or regulated information unless that use is approved for the configured Google service.

Risk: Dependencies are declared with minimum versions rather than pinned versions.

Mitigation: Install in an isolated environment and pin reviewed dependency versions for controlled deployments.

## Reference(s):

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Google Custom Search Documentation](https://cloud.google.com/custom-search/docs)
- [Custom Search JSON API Reference](https://developers.google.com/custom-search/v1/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown-formatted search results and setup guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include titles, URLs, snippets, and display links; Google Custom Search returns up to 10 results per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
