## Description:

Searches YouTube videos, channels, and playlists through the AIsa unified API using an AISA_API_KEY, without requiring a Google API key or OAuth setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to discover YouTube videos, channels, and playlists, localize searches with country and language parameters, paginate results, and produce code or shell-command examples for the AIsa YouTube search endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access to AIsa with the user's AISA_API_KEY.

Mitigation: Install only when that network access and credential use are acceptable for the deployment environment.

Risk: The documentation includes troubleshooting guidance that can print the API key into logs or terminal history.

Mitigation: Use a presence check instead of echoing the key, and rotate the key if it has appeared in logs.

Risk: The documentation includes LLM and web-search examples beyond the core YouTube-search scope.

Mitigation: Avoid those examples unless the deployment explicitly intends to use the separate AIsa services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-youtube)
- [AIsa API Documentation](https://docs.aisa.one)
- [AIsa Dashboard / Marketplace](https://marketplace.aisa.one)
- [YouTube Search API Reference](https://docs.aisa.one/reference/get_youtube-search)
- [AIsa Smart Search API](https://docs.aisa.one/reference/get_search-smart)
- [AIsa Chat Completions API](https://docs.aisa.one/reference/createchatcompletion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and inline Python, JavaScript, and curl snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request parameters, pagination-token handling, localization options, and response-parsing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
